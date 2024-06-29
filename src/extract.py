import re
from pathlib import Path

from tqdm import tqdm
import yaml
from llama_index.core import (
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.indices.struct_store import JSONQueryEngine

from .helpers import KPI, Report, RevDriver, Summary, list_json_files

########################################################################################
# Templates
########################################################################################
DRIVER_TMPL = (
    "make a short summary about the major drivers behind {}s revenue change in {}?"
)

KPI_TMPL = (
    "Your job is to find a Key Performance indicator (KPI) for {} and format/return it "
    "in the base number system (not Million/Billion) as well as retrieve the currency.\n"
    "------------------------------------\n"
    "Example:\n"
    "IBM's revenue for the year was $61.9 billion. -> 61900000000\n"
    "------------------------------------\n"
    "find the {} KPI\n"
    "------------------------------------\n"
    "the output is only the formatted number and currency and nothing else!\n"
    "if you don't find the KPI, output 'KPI not found'\n"
    "------------------------------------\n"
    "Example output where KPI is found:\n"
    "61900000000, $"
    "Example output where KPI is NOT found:\n"
    "KPI not found"
)

########################################################################################
# helper funcs
########################################################################################


def get_numbers_in_brackets(s: str) -> list[int]:
    numbers = re.findall(r"\[(\d+)\]", s)
    numbers = [int(num) for num in numbers]
    return numbers


def get_revdriver(index, rep: Report, top_k: int):
    query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=top_k,
        citation_chunk_size=512,
    )
    response = query_engine.query(DRIVER_TMPL.format(rep.company, rep.year))
    bracket_nums = get_numbers_in_brackets(response.response)
    context = [response.source_nodes[i - 1].get_text() for i in bracket_nums]
    return RevDriver(content=response.response, context=context)


def get_kpi(index, rep: Report, kpi: str):
    query_engine = index.as_query_engine(response_mode="refine")
    response = query_engine.query(KPI_TMPL.format(rep.company, kpi))
    context = response.source_nodes[0].get_text()

    # extract pattern from input string
    pattern = r"(\d+),\s*([^\d\s]+)"
    match = re.search(pattern, response.response)
    if match:
        number = match.group(1)
        currency = match.group(2)
    else:
        number = "-1"
        currency = "-1"

    return KPI(name=kpi, value=float(number), currency=currency, context=context)


########################################################################################
# main
########################################################################################


def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_r = Path(cfg["data"]["chunk"])
    path_i = Path(cfg["data"]["index"])
    path_o = Path(cfg["data"]["summary"])
    kpi_list = cfg["kpis"]

    # model
    embed_model = AzureOpenAIEmbedding(**cfg["models"]["embed_model"])
    llm = AzureOpenAI(**cfg["models"]["llm"])

    # settings
    Settings.llm = llm
    Settings.embed_model = embed_model

    # parse reports
    files = list_json_files(path_r)
    reports = [Report.load(f) for f in files]

    # summary
    for rep in tqdm(reports):
        idx = load_index_from_storage(
            StorageContext.from_defaults(
                persist_dir=str(path_i / f"{rep.year}_{rep.company}.idx")
            )
        )

        rev_driver = get_revdriver(idx, rep, 3)
        kpis = [get_kpi(index=idx, rep=rep, kpi=kpi) for kpi in kpi_list]
        kpis = [kpi for kpi in kpis if kpi.value > 0]

        # dump
        sum = Summary(
            company=rep.company, year=rep.year, rev_driver=rev_driver, kpis=kpis
        )
        sum.save(path_o)


if __name__ == "__main__":
    main()

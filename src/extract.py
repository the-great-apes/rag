import re
from pathlib import Path
import os

from tqdm import tqdm
import yaml
from llama_index.core import (
    Settings,
    StorageContext,
    load_index_from_storage,
    PromptTemplate,
)
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.groq import Groq
from llama_index.core.indices.struct_store import JSONQueryEngine

from .helpers import KPI, Report, Driver, Summary, list_json_files

########################################################################################
# Templates
########################################################################################

KPI_TMPL = ()
PROMPTS = yaml.safe_load(open("params.yaml"))["extraction"]["templates"]

########################################################################################
# helper funcs
########################################################################################


def get_numbers_in_brackets(s: str) -> list[int]:
    numbers = re.findall(r"\[(\d+)\]", s)
    numbers = [int(num) for num in numbers]
    return numbers


def get_driver(index, rep: Report, kpi: str, cite_ch_size: int, top_k: int):
    query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=top_k,
        citation_chunk_size=cite_ch_size,
        response_mode="compact_accumulate",
    )
    prompt_template = PromptTemplate(PROMPTS["driver"]).format(
        company=rep.company, kpi=kpi, year=rep.year
    )
    response = query_engine.query(prompt_template)
    bracket_nums = get_numbers_in_brackets(response.response)
    context = [response.source_nodes[i - 1].get_text() for i in bracket_nums]
    return Driver(content=response.response, context=context)


def get_kpi(index, rep: Report, kpi: str, cite_ch_size: int):
    query_engine = CitationQueryEngine.from_args(
        index,
        similarity_top_k=3,
        citation_chunk_size=cite_ch_size,
        response_mode="compact_accumulate",
    )
    prompt_template = PromptTemplate(PROMPTS["kpi"]).format(
        company=rep.company, kpi=kpi, year=rep.year
    )
    response = query_engine.query(prompt_template)
    context = response.source_nodes[0].get_text()

    # extract pattern from input string
    pattern = r"(\d+),\s*([^\d\s]+)"
    match = re.search(pattern, response.response)
    if match:
        number = match.group(1)
        currency = match.group(2)
        driver = get_driver(
            index=index, rep=rep, kpi=kpi, cite_ch_size=cite_ch_size, top_k=3
        )
    else:
        number = "-1"
        currency = "-1"
        driver = Driver(content="", context=[])

    return KPI(
        name=kpi, value=float(number), currency=currency, context=context, driver=driver
    )


########################################################################################
# main
########################################################################################


def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_r = Path(cfg["data"]["chunk"])
    path_i = Path(cfg["data"]["index"])
    path_o = Path(cfg["data"]["summary"])
    kpi_list = cfg["extraction"]["kpis"]
    citation_chunk_size = cfg["extraction"]["citation_chunk_size"]

    # model
    if cfg["use_openai"]:
        embed_model = AzureOpenAIEmbedding(**cfg["models"]["embed_openai"])
        llm = AzureOpenAI(**cfg["models"]["openai"])
    else:
        embed_model = HuggingFaceEmbedding(model_name=cfg["models"]["embed_local"]["model"],
                                           device=os.environ.get("EMBEDDING_DEVICE"))
        llm = Groq(model=cfg["models"]["groq"]['deployment_name'],
                   api_key=os.environ.get("GROQ_API_KEY"))

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

        kpis = [
            get_kpi(index=idx, rep=rep, kpi=kpi, cite_ch_size=citation_chunk_size)
            for kpi in kpi_list
        ]
        kpis = [kpi for kpi in kpis if kpi.value > 0]

        # dump
        sum = Summary(company=rep.company, year=rep.year, kpis=kpis)
        sum.create_summary()
        sum.save(path_o)


if __name__ == "__main__":
    main()

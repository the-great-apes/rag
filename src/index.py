from pathlib import Path

import yaml
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
from tqdm import tqdm
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI

from .helpers import Report, list_json_files

########################################################################################
# main
########################################################################################


def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_i = Path(cfg["data"]["chunk"])
    path_o = Path(cfg["data"]["index"])

    # model
    embed_model = AzureOpenAIEmbedding(**cfg["models"]["embed_model"])
    llm = AzureOpenAI(**cfg["models"]["llm"])

    # settings
    Settings.llm = llm
    Settings.embed_model = embed_model

    # parse files
    files = list_json_files(path_i)
    reports = [Report.load(f) for f in files]

    # save index
    for r in tqdm(reports):
        path = path_o / f"{r.year}_{r.company}.idx"
        documents = [Document(doc_id=c.id, text=c.content) for c in r.chunks]
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=path)


if __name__ == "__main__":
    main()

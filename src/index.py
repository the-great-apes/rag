from pathlib import Path
import os

import yaml
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
from tqdm import tqdm
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.groq import Groq

from .helpers import Report, list_json_files
from .local_models.phi3 import Phi3

########################################################################################
# main
########################################################################################

cfg = yaml.safe_load(open("params.yaml"))

def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_i = Path(cfg["data"]["chunk"])
    path_o = Path(cfg["data"]["index"])

    # model
    if cfg['model_to_use'] == "openai":
        embed_model = AzureOpenAIEmbedding(**cfg["models"]["embed_openai"])
        llm = AzureOpenAI(**cfg["models"]["openai"])
    elif cfg['model_to_use'] == "groq":
        embed_model = HuggingFaceEmbedding(model_name=cfg["models"]["embed_local"]["model"],
                                           device=os.environ.get("EMBEDDING_DEVICE"))
        llm = Groq(model=cfg["models"]["groq"]['deployment_name'],
                   api_key=os.environ.get("GROQ_API_KEY"))
    else:
        embed_model = HuggingFaceEmbedding(model_name=cfg["models"]["embed_local"]["model"],
                                           device=os.environ.get("EMBEDDING_DEVICE"))
        llm =  Phi3(cfg["models"]["hf_phi3"]['model']).get_llm()

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

from llama_index.core import Document
from tqdm import tqdm
import yaml
from pathlib import Path
import os

from .helpers import Report, Chunk, list_json_files

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


########################################################################################
# helper funcs
########################################################################################


def chunk_text(
    text: str, embed_model, buffer_size: int, percentile_threshold: int
) -> list[str]:
    """
    Splits the given text into chunks of specified size with overlap.

    :param text: The input text to be chunked.
    :param buffer_size: number of sentences to group together
    :param percentile_threshold: determines the sensitivity of the splitting mechanism
    :return: A list of text chunks.
    """
    splitter = SemanticSplitterNodeParser(
        buffer_size=buffer_size,
        breakpoint_percentile_threshold=percentile_threshold,
        embed_model=embed_model,
    )
    nodes = splitter.get_nodes_from_documents([Document(text=text)])
    return [n.get_content() for n in nodes]


########################################################################################
# main
########################################################################################
cfg = yaml.safe_load(open("params.yaml"))
use_openai = cfg['model_to_use'] == "openai"
print(f"use_openai: {use_openai}")

def main():
    cfg = yaml.safe_load(open("params.yaml"))
    path_i = Path(cfg["data"]["clean"])
    path_o = Path(cfg["data"]["chunk"])
    chunk_buffer_size = cfg["chunking"]["buffer_size"]
    chunk_percentile_threshold = cfg["chunking"]["percentile_threshold"]

    # model
    if use_openai:
        embed_model = AzureOpenAIEmbedding(**cfg["models"]["embed_openai"])
    else:
        embed_model = HuggingFaceEmbedding(model_name=cfg["models"]["embed_local"]["model"],
                                           device=os.environ.get("EMBEDDING_DEVICE"))

    # parse files
    files = list_json_files(path_i)
    reports = [Report.load(f) for f in files]

    # chunk
    for r in tqdm(reports):
        chunks = chunk_text(
            text=r.content,
            embed_model=embed_model,
            buffer_size=chunk_buffer_size,
            percentile_threshold=chunk_percentile_threshold,
        )
        for i, c in enumerate(chunks):
            r.chunks.append(Chunk(id=str(i), content=c))

    # dump
    for r in tqdm(reports):
        r.save(path_o)


if __name__ == "__main__":
    main()

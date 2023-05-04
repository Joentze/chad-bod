import json
import os
import re
from os import listdir
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import keys

chroma = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chromadb"
))
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="", model_name="text-embedding-ada-002")


def compile_all_documents(path: str) -> None:
    """gets all vector documents and generates a compiled file for chroma loading"""
    documents = []
    sources = []
    for this_file in listdir("./"+path):
        with open(f"./{path}/{this_file}", "r", encoding="utf-8") as file:
            obj = json.load(file)
            documents += [re.sub(r'[^\w]', ' ', document)
                          for document in obj["documents"]]
            sources += obj["sources"]
    with open("compiled.json", "w", encoding="utf-8") as file:
        json.dump({"documents": documents, "sources": sources}, file)


def init_chroma(collection_name: str, compiled_file_path: str) -> object:
    """initialies vector db"""

    with open(compiled_file_path, "r", encoding="utf-8") as file:
        content = json.load(file)
        documents = content["documents"]
        sources = content["sources"]
        sources = [{"source": source} for source in sources]
        filtered_docs = []
        filtered_srcs = []
        ids = []

    collection = chroma.create_collection(
        name=collection_name, embedding_function=ef)
    if len(sources) == len(documents):
        for i in range(len(documents)):
            if len(documents[i]) > 20:
                filtered_docs.append(documents[i])
                filtered_srcs.append(sources[i])
                ids.append(f"id_{i}")

    collection.add(documents=filtered_docs[:2040], metadatas=filtered_srcs[:2040],
                   ids=ids[:2040])
    collection.add(documents=filtered_docs[2041:], metadatas=filtered_srcs[2041:],
                   ids=ids[2041:])

    return collection


if __name__ == "__main__":
    # compile_all_documents("vector_documents")
    # collection = init_chroma("smu_facts", "./compiled.json")
    collection = chroma.get_collection("smu_facts", embedding_function=ef)
    results = collection.query(
        query_texts=["when smu connexion opened"],
        n_results=2,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    print(results)

"""Instantiates Vector Database, ChromaDB, and adds data into collection"""

import json
from os import listdir
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from secret_keys import OPEN_AI_KEY

COLLECTION_JSON = "compiled.json"

chroma = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chromadb"
))
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPEN_AI_KEY, model_name="text-embedding-ada-002")


def compile_all_documents(path: str) -> None:
    """gets all vector documents and generates a compiled file for chroma loading"""
    documents = []
    sources = []
    for this_file in listdir(f"./{path}"):
        with open(f"./{path}/{this_file}", "r", encoding="utf-8") as file:
            obj = json.load(file)
            documents += [document
                          for document in obj["documents"]]
            sources += obj["sources"]
    with open(COLLECTION_JSON, "w", encoding="utf-8") as file:
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
        for i, document in enumerate(documents):
            # only add documents with more than 20 characters long
            if len(document) > 20:
                filtered_docs.append(document)
                filtered_srcs.append(sources[i])
                ids.append(f"id_{i}")

    load_into_collection_by_chunks(
        filtered_docs=filtered_docs, filtered_srcs=filtered_srcs, ids=ids, chunk_size=2000, collection=collection)

    return collection


def load_into_collection_by_chunks(filtered_docs, filtered_srcs, ids, chunk_size, collection):
    """add chunks into chroma db"""
    if len(filtered_docs) != len(filtered_srcs) or len(filtered_srcs) != len(ids) or len(filtered_docs) != len(ids):
        return
    else:
        num_of_chunks = len(filtered_docs)//chunk_size
        for i in range(num_of_chunks):
            start = i*chunk_size
            end = (i+1)*chunk_size
            collection.add(documents=filtered_docs[start:end], metadatas=filtered_srcs[start:end],
                           ids=ids[start:end])


def get_contexts(question: str, collection, num_of_results):
    """returns chunk of contexts from chroma"""
    contexts = []
    collection = chroma.get_collection("smu_facts", embedding_function=ef)
    results = collection.query(
        query_texts=[question],
        n_results=num_of_results,
    )
    documents = results["documents"][0]
    sources = results["metadatas"][0]
    for idx, document in enumerate(documents):
        link = sources[idx]["source"]
        context = f"- {document} [source]({link})"
        contexts.append(context)
    return "\n".join(contexts)


if __name__ == "__main__":
    compile_all_documents("vector_documents")
    init_chroma("smu_facts", f"./{COLLECTION_JSON}")

    # print(results)

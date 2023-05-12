"""adds documents in supabase vector database"""
import json
from typing import List
from os import listdir, environ
import openai
from openai.embeddings_utils import get_embedding
from supabase import create_client

# open ai details
openai.api_key = environ["OPENAI_API_KEY"]
# supabase details
supabase_url = environ["SUPABASE_URL"]
supabase_key = environ["SUPABASE_KEY"]
supabase = create_client(supabase_url=supabase_url, supabase_key=supabase_key)

COLLECTION_JSON = "compiled.json"


def compile_all_documents(path: str) -> None:
    """gets all vector documents and generates a compiled file for chroma loading"""
    documents = {"documents": []}
    for this_file in listdir(f"./{path}"):
        with open(f"./{path}/{this_file}", "r", encoding="utf-8") as file:
            obj = json.load(file)
            docs = obj["documents"]
            srcs = obj["sources"]
            if len(docs) == len(srcs):
                documents["documents"] += [{"content": docs[i], "source":srcs[i]}
                                           for i in range(len(docs))]
    with open(COLLECTION_JSON, "w", encoding="utf-8") as file:
        json.dump(documents, file)


def get_embeddings(document: str) -> List[float]:
    """get open ai embedding"""
    try:
        embedding = get_embedding(
            text=document, engine="text-embedding-ada-002")
        return embedding
    except Exception as error:
        print(
            error, f"The following document cannot be embedded at this time {document}")


def write_to_supabase(documents: List[object]):


def push_embeddings(compiled_json_file: str):
    with open(compiled_json_file, "r", encoding="utf-8") as file:
        documents = json.load(file)["documents"]
    for document in documents[:10]:
        content = document["content"]
        embedding = get_embedding(content)

from chromadb import Client


def init_chroma(collection_name: str) -> None:
    chroma = Client()
    collection = chroma.create_collection(name=collection_name)
    

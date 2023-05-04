from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup

results = []


def get_meta_tags(links):
    for link in links:
        response = requests.get(link, timeout=10000)
        soup = BeautifulSoup(response.text)

        metas = soup.find_all('meta')

        description = " ".join([meta.attrs['content']
                                for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description'])
        print(description)
        results.append({"url": link, "description": description})


if __name__ == "__main__":
    documents = []
    sources = []
    with open("./data/smu_blog_desc.json", "r", encoding="utf-8") as file:
        obj = json.load(file)
        blogs = obj["data"]
        for blog in blogs:
            documents.append(blog["description"].strip())
            sources.append(blog["url"])
    with open("./vector_documents/blogs.json", "w", encoding="utf-8") as file:
        json.dump({"documents": documents, "sources": sources}, file)

    # with open("./data/smu_blog_desc.json", "w", encoding="utf-8") as file:

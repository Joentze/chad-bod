import json
from pprint import pprint
# src: https://www.smu.edu.sg/sites/default/files/smu/campus-life/SMU%20-%20Frequently%20Asked%20Questions%20_02022023.pdf

with open("./data/travel_insurance.json", "r") as json_file:
    faqs = json.load(json_file)["data"]
    documents = [" ".join(faq.split(".")[1:]).strip() for faq in faqs]
    sources = [
        "https://www.smu.edu.sg/sites/default/files/smu/campus-life/SMU%20-%20Frequently%20Asked%20Questions%20_02022023.pdf" for i in range(len(faqs))]
with open("./vector_documents/travel_insurance.json", "w", encoding="utf-8") as file:
    json.dump({"documents": documents, "sources": sources}, file)

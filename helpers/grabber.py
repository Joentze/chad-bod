import json

# is_running = True

# while is_running:
#     text = input("what is the next set of text")
#     if text == "/stop":
#         is_running = False
#         break

#     with open("../data/grabber_dump.json", "r", encoding="utf-8") as file:
#         obj = json.load(file)

#     with open("../data/grabber_dump.json", "w", encoding="utf-8") as file:
#         obj["data"].append(text)
#         json.dump(obj, file)
with open("./data/smu_ccas.txt", "r") as file:
    obj = {"documents": [], "sources": []}
    for line in file.readlines():
        obj["documents"].append(line)
        obj["sources"].append(
            "https://www.smu.edu.sg/sites/default/files/smu/campus-life/%5BPDF%5D%20Clubs%20and%20Societies%20v4.pdf")

with open("./vector_documents/ccas.json", "w", encoding="utf-8") as file:
    json.dump(obj, file)

import json
from pprint import pprint
# src: https://www.smu.edu.sg/sites/default/files/smu/campus-life/SMU%20-%20Frequently%20Asked%20Questions%20_02022023.pdf
with open("./data/travel_insurance_faq.txt", "r", encoding="utf-8") as file:
    text = file.read()
    with open("./data/travel_insurance.json", "w") as json_file:
        json.dump({"data": [ans.strip().replace("\n", " ")
                  for ans in text.split("===")]}, json_file)

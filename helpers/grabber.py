import json

is_running = True

while is_running:
    text = input("what is the next set of text")
    if text == "/stop":
        is_running = False
        break

    with open("../data/grabber_dump.json", "r", encoding="utf-8") as file:
        obj = json.load(file)

    with open("../data/grabber_dump.json", "w", encoding="utf-8") as file:
        obj["data"].append(text)
        json.dump(obj, file)

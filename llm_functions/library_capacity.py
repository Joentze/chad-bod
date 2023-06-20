import json
from requests import get

url = "https://smulibraries.southeastasia.cloudapp.azure.com/public/count.json"


def get_library_numbers(library: str) -> str:
    """gets the current number of people inside smu libraries"""
    try:
        response = get(url=url, timeout=5000)
        response_obj = json.loads(response.text)
        number = response_obj[library]["inside"]
        return f"There are {number} people."
    except:
        return "It seems like the Library API is down. Please try again later!"


if __name__ == "__main__":
    pass

import json
from requests import post
from pprint import pprint

FACULTY_URL = "https://gfhoramcbe-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.17.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.54.1)%3B%20JS%20Helper%20(3.11.3)&x-algolia-api-key=a28a8f8d535aa316186829a05cb858e1&x-algolia-application-id=GFHORAMCBE"


def get_faculty(page_start: int, page_end: int):
    """get all faculty details"""
    all_faulty = []
    for page_no in range(page_start, page_end+1):
        json_body = {"requests": [
            {"indexName": "faculty", "params":
             f"facets=%5B%22profiletype%22%2C%22strategicpriorities%22%2C%22school%22%2C%22societalchallenges.lvl0%22%2C%22researcharea.lvl0%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=1000&page={page_no}&query=&tagFilters="}
        ]
        }
        print(json_body)
        response = post(headers={"Content-Type": "application/json", "x-algolia-agent": "Algolia%20for%20JavaScript%20(4.17.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.54.1)%3B%20JS%20Helper%20(3.11.3)",
                                 "x-algolia-api-key": "a28a8f8d535aa316186829a05cb858e1", "x-algolia-application-id": "GFHORAMCBE"}, url=FACULTY_URL, json=json_body, timeout=10000)
        data = response.json()
        hits = data["results"][0]["hits"]
        persons = [{"name": hit["name"].strip().lower(), "school":hit["school"].lower(),
                    "phone":hit["phone"], "url":hit["url"],"email":hit["email"]}for hit in hits]
        all_faulty += persons
    return all_faulty


if __name__ == "__main__":
    with open("./data/faculty.json", "w", encoding="utf-8") as file:
        faculty = get_faculty(0, 30)
        print(len(faculty))
        json.dump({"data": faculty}, file)

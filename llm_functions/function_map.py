from llm_functions.library_capacity import get_library_numbers

function_map = {
    "get_library_numbers": get_library_numbers
}

llm_functions = [{"name": "get_library_numbers",
                  "description": "gets the number of people in kgc (kwa geok choo) or lks (li ka shing) library",
                  "parameters": {
                      "type": "object",
                      "properties": {
                          "library": {'title': 'library to check numbers on ', 'type': 'string', "enum": ["kgc", "lks"]},
                      },
                      "required": ["url"],
                  }}]

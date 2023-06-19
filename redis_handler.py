"""Redis handler"""
import ast
from typing import List
from pprint import pprint
from redis import Redis


MAX_MESSAGE_MEMORY_SIZE = 5

test_history = {
    "messages": [
        {"role": "assistant", "content": "hello"},
        {"role": "user", "content": "hi there"},
        {"role": "assistant", "content": "im good"},
        {"role": "user", "content": "im good too"},
        {"role": "assistant", "content": "thanks"},
    ]
}

r = Redis(host="localhost", port="32768", password="redispw")


def sets_message_history(chat_id: str, message_history: object) -> bool:
    """sets message history for chat id"""
    try:
        str_obj = str(message_history)
        r.set(name=chat_id, value=str_obj)
        return True
    except:
        return False


def get_message_history(chat_id: str) -> List[object]:
    """gets message history for chat id"""
    try:
        response = r.get(name=chat_id).decode("utf-8")
        response_obj = ast.literal_eval(response)
        return response_obj["messages"]
    except:
        return None


def insert_message_history(chat_id: str, message: object) -> bool:
    history = get_message_history(chat_id)
    if history:
        if len(history) < MAX_MESSAGE_MEMORY_SIZE:
            history.append(message)
        elif len(history) == MAX_MESSAGE_MEMORY_SIZE:
            history.pop(0)
            history.append(message)
        return sets_message_history(chat_id=chat_id, message_history={
            "messages": history})
    return sets_message_history(chat_id=chat_id, message_history={
        "messages": [message]})


if __name__ == "__main__":
    # sets_message_history("0000", test_history)
    insert_message_history(
        "0000", {"role": "user", "content": "what is the weather like today"})
    response = get_message_history("0000")
    pprint(response)

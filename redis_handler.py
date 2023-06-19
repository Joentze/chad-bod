"""Redis handler"""
import os
import ast
from typing import List
from pprint import pprint
from redis import Redis


MAX_MESSAGE_MEMORY_SIZE = 5
REDIS_ENDPOINT = os.environ["REDIS_ENDPOINT"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

test_history = {
    "messages": [
        {"role": "assistant", "content": "hello"},
        {"role": "user", "content": "hi there"},
        {"role": "assistant", "content": "im good"},
    ]
}

r = Redis(host=REDIS_ENDPOINT, port=REDIS_PORT, password=REDIS_PASSWORD)


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
    """manages insertion of messages"""
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


def delete_user_from_redis(chat_id: str) -> bool:
    """deletes user from redis"""
    try:
        r.delete(chat_id)
        return True
    except:
        return False


if __name__ == "__main__":
    response = sets_message_history("TEST", "TEST")
    # insert_message_history(
    #     "0000", {"role": "user", "content": "what is the weather like today"})
    # response = get_message_history("0000")
    pprint(response)

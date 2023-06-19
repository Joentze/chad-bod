# from google.cloud import pubsub_v1
from threading import Thread
import ast
import os
# import json
import base64
from flask import Flask, request
from chat_bot_main import respond_with_llm, is_within_token_limit, EXCEED_TOKEN_MESSAGE
from telegram_helper import reply_loading, send_message
from secret_keys import TELEGRAM_API_KEY
from tele_messages import STARTER_MESSAGE
from build_supabase import add_new_user, remove_user

app = Flask(__name__)

PORT = int(os.environ["PORT"])


def check_post_data_format(envelope):
    if not envelope:
        return True
    if not isinstance(envelope, dict) or "message" not in envelope:
        return True
    return False


def message_obj(pubsub_message):
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        string_obj = base64.b64decode(
            pubsub_message["data"]).decode("utf-8").strip()
        return ast.literal_eval(string_obj)


@app.route("/", methods=["POST"])
def index():

    def llm_run(configs):
        respond_with_llm(configs)
    response = request.get_json()
    # print(response)
    if "message" in response:
        chat_id = response["message"]["chat"]["id"]
        username = response["message"]["chat"]["username"]
        query = response["message"]["text"]
        if is_within_token_limit(query) is False:
            send_message(TELEGRAM_API_KEY, chat_id, EXCEED_TOKEN_MESSAGE)
            return ("Exceeded token limit!", 204)
    else:
        return ("Message was probably edited", 204)
    if query == "/start":
        send_message(TELEGRAM_API_KEY, chat_id, STARTER_MESSAGE)
        add_new_user(chat_id=chat_id, username=username)
        return ("", 204)
    if query == "/stop":
        remove_user(chat_id)
        return ("", 204)
    get_loading_message = reply_loading(TELEGRAM_API_KEY, chat_id)
    loading_response = ast.literal_eval(
        get_loading_message.text.replace("true", "True").replace("false", "False"))
    message_id = loading_response["result"]["message_id"]
    config = {"chat_id": chat_id, "message_id": message_id, "query": query}
    try:
        thread = Thread(target=llm_run, kwargs={"configs": config})
        thread.start()
        thread.join()
    except:
        return ("", 500)

    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)

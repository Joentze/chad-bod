# from google.cloud import pubsub_v1
from threading import Thread
import ast
import os
# import json
import base64
from flask import Flask, request
from chat_bot_main import respond_with_llm
from telegram_helper import reply_loading
from secret_keys import TELEGRAM_API_KEY


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
    chat_id = response["message"]["chat"]["id"]
    query = response["message"]["text"]
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

# from google.cloud import pubsub_v1
from threading import Thread
import ast
import os
# import json
import base64
from flask import Flask, request

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
        

    envelope = request.get_json()

    if check_post_data_format(envelope):
        return "Bad Request: Check Gcloud Pub/Sub message formating or message body type", 400

    pubsub_message = envelope["message"]

    data_configs = message_obj(pubsub_message)

    if data_configs and "configs" in data_configs:
        thread = Thread(target=llm_run, kwargs={
                        "configs": data_configs["configs"]})
        thread.start()
        thread.join()
    else:
        return ("", 400)

    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)

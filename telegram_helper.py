"""Telegram Bot Helpers"""
import os
import urllib.parse
from requests import get, Response


def edit_message(API_KEY: str, message_id: str, chat_id: str, new_message: str) -> Response:
    """edits telegram message"""
    new_message = urllib.parse.quote(new_message.replace('.', '\\.').replace('+', '\\+').replace('!', '\\!').replace('<', '\\<').replace('>', '\\>').replace(',', '\\,').replace('/', '\\/').replace(
        '_', '\\_').replace("[", "\\[").replace(']', '\\]').replace("-", "\\-").replace('(', '\\(').replace(')', '\\)').encode("utf-8"))

    return get(url=f"https://api.telegram.org/bot{API_KEY}/editMessageText?message_id={message_id}&chat_id={chat_id}&text={new_message}&parse_mode=MarkdownV2",
               timeout=10000)


def reply_loading(API_KEY: str, chat_id: str):
    """sends loading buffer text"""
    return get(f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={chat_id}&text=```Loading...```&parse_mode=MarkdownV2", timeout=10000)


if __name__ == "__main__":
    # print(ast.literal_eval(reply_loading(os.environ["TELEGRAM_API_KEY"], 549991017).text.replace("true","True").replace("false","False"))["result"]["message_id"])
    edit_message(os.environ["TELEGRAM_API_KEY"], 73, 549991017, "even lamer")

"""Telegram Bot Helpers"""
import urllib.parse
from requests import get, Response


def edit_message(API_KEY: str, message_id: str, chat_id: str, new_message: str) -> Response:
    """edits telegram message"""
    new_message = urllib.parse.quote(
        escpae_symbols(new_message).encode("utf-8"))
    return get(url=f"https://api.telegram.org/bot{API_KEY}/editMessageText?message_id={message_id}&chat_id={chat_id}&text={new_message}&parse_mode=MarkdownV2",
               timeout=10000)


def reply_loading(API_KEY: str, chat_id: str):
    """sends loading buffer text"""
    return get(f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={chat_id}&text=```Loading...```&parse_mode=MarkdownV2", timeout=10000)


def send_message(API_KEY: str, chat_id: str, new_message: str) -> Response:
    """send telegram message"""
    new_message = urllib.parse.quote(
        escpae_symbols(new_message).encode("utf-8"))
    return get(url=f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={chat_id}&text={new_message}&parse_mode=MarkdownV2&disable_web_page_preview=true",
               timeout=10000)


def escpae_symbols(message: str) -> str:
    """Escapes symbols for telegram message"""
    return message.replace('.', '\\.').replace('+', '\\+').replace('!', '\\!').replace('<', '\\<').replace('>', '\\>').replace(',', '\\,').replace('/', '\\/').replace(
        '_', '\\_').replace("[", "\\[").replace(']', '\\]').replace("-", "\\-").replace('(', '\\(').replace(')', '\\)')


if __name__ == "__main__":

    pass

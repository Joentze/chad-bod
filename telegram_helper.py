"""Telegram Bot Helpers"""

from requests import get, Response


def edit_message(API_KEY: str, message_id: str, chat_id: str, new_message: str) -> Response:
    """edits telegram message"""
    return get(url=f"https://api.telegram.org/bot{API_KEY}/editMessageText?message_id={message_id}&chat_id={chat_id}&text={new_message}&parse_mode=MarkdownV2",
               timeout=10000)

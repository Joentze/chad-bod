"""Running LLM Scripts"""
from typing import List
from datetime import datetime
from dataclasses import dataclass
from openai import ChatCompletion
from secret_keys import TELEGRAM_API_KEY, OPEN_AI_KEY
from langchain import LLMChain
from langchain.llms import OpenAI
from build_supabase import get_context_from_supabase
from prompts import get_prompt, insert_context_to_prompt
from telegram_helper import edit_message
from redis_handler import insert_message_history, get_message_history

MODEL_NAME = "text-davinci-003"
MAX_NUM_TOKEN_TELEGRAM = 50
EXCEED_TOKEN_MESSAGE = """```You've exceeded the token limit for this message, please rephrase into a shorter statement...```"""


davinci = OpenAI(model_name=MODEL_NAME,
                 openai_api_key=OPEN_AI_KEY, temperature=0, max_tokens=1000)


@dataclass
class TelegramQuery:
    chat_id: str
    message_id: str
    query: str


def is_within_token_limit(message: str) -> bool:
    """checks if message sent is within character limit"""
    return len(message)//4 <= MAX_NUM_TOKEN_TELEGRAM


def run_llm(question: str):
    """runs open ai llm"""
    contexts = get_context_from_supabase(question, 0.8, 3)
    llm_chain = LLMChain(prompt=get_prompt(contexts), llm=davinci)
    response = llm_chain.run(question)
    return response


def respond_with_llm(configs):
    """edits specific telegram bot message"""
    query = TelegramQuery(
        chat_id=configs["chat_id"], message_id=configs["message_id"], query=configs["query"])
    messages = get_message_history(query.chat_id)
    response = chat_completion(query.chat_id, query.query, messages)
    edit_message(API_KEY=TELEGRAM_API_KEY, message_id=query.message_id,
                 chat_id=query.chat_id, new_message=response)


def chat_completion(chat_id: str, curr_query: str, history: List[object]) -> str:
    """sends query to LLM"""
    contexts = get_context_from_supabase(curr_query, 0.8, 3)
    prompt = insert_context_to_prompt(curr_query, contexts)
    messages = [
        {"role": "system", "content": "You are Chad Bod, a Singapore Management University Student Helper"},
        *history,
        {"role": "user", "content": prompt}
    ],
    print(messages)
    completion = ChatCompletion.create(
        model=MODEL_NAME,
        temperature=0,
        messages=messages
    )

    message = completion.choices[0].message
    insert_message_history(chat_id=chat_id, message={
                           "role": "assistant", "content": message})
    return message


if __name__ == "__main__":
    t1 = datetime.now()
    print(run_llm("how many libraries are there in smu"))

    # respond_with_llm({
    #     "chat_id": 549991017,
    #     "message_id": 73,
    #     "query": "what are the requirements for dean's list"
    # })
    print("total time taken: ", datetime.now()-t1)

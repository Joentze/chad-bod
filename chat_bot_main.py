"""Running LLM Scripts"""
from datetime import datetime
from dataclasses import dataclass
from secret_keys import TELEGRAM_API_KEY, OPEN_AI_KEY
from langchain import LLMChain
from langchain.llms import OpenAI
from build_supabase import get_context_from_supabase
from prompts import get_prompt
from telegram_helper import edit_message


MAX_NUM_TOKEN_TELEGRAM = 60
EXCEED_TOKEN_MESSAGE = """```You've exceeded the token limit for this message, please rephrase into a shorter statement...```"""


davinci = OpenAI(model_name='text-davinci-003',
                 openai_api_key=OPEN_AI_KEY, temperature=0, max_tokens=256)


@dataclass
class TelegramQuery:
    chat_id: str
    message_id: str
    query: str


def is_within_token_limit(message: str) -> bool:
    """checks if message sent is within character limit"""
    return len(message) <= MAX_NUM_TOKEN_TELEGRAM


def run_llm(question: str):
    """runs open ai llm"""
    contexts = get_context_from_supabase(question, 0.7, 5)
    llm_chain = LLMChain(prompt=get_prompt(contexts), llm=davinci)
    response = llm_chain.run(question)
    return response


def respond_with_llm(configs):
    """edits specific telegram bot message"""
    query = TelegramQuery(
        chat_id=configs["chat_id"], message_id=configs["message_id"], query=configs["query"])
    response = run_llm(question=query.query)
    print("llm response: ", response, "message_id",
          query.message_id, "chat_id", query.chat_id)
    print(edit_message(API_KEY=TELEGRAM_API_KEY, message_id=query.message_id,
                       chat_id=query.chat_id, new_message=response).text)


if __name__ == "__main__":
    t1 = datetime.now()
    # print(run_llm("how do i bid for a mod"))

    respond_with_llm({
        "chat_id": 549991017,
        "message_id": 73,
        "query": "what is smu cru"
    })
    print("total time taken: ", datetime.now()-t1)

from langchain.llms import OpenAI
from langchain import LLMChain
from build_chroma_db import get_contexts, chroma, ef
from prompts import get_prompt
davinci = OpenAI(model_name='text-davinci-003',
                 openai_api_key="",temperature=0)
collection = chroma.get_collection("smu_facts", embedding_function=ef)


def run_llm(question: str, collection):
    contexts = get_contexts(question, collection, 5)
    llm_chain = LLMChain(prompt=get_prompt(contexts), llm=davinci)
    return llm_chain.run(question)


if __name__ == "__main__":
    print(run_llm("what does smu travel insurance cover", collection))

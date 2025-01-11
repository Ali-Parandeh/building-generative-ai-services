# main.py

from fastapi import FastAPI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI(openai_organization="YOUR_ORGANIZATION_ID")
template = """
Your name is FastAPI bot and you are a helpful
chatbot responsible for teaching FastAPI to your users.
Here is the user query: {query}
"""
prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(prompt=prompt, llm=llm)

app = FastAPI()


@app.get("/generate/text")
def generate_text_controller(query: str):
    return llm_chain.run(query)

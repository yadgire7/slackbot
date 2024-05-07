# import required libraries
import os
from langchain.llms import OpenAI, HuggingFaceHub
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain, APIChain
from langchain_experimental.pal_chain.base import  PALChain
from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains.api import open_meteo_docs
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv, find_dotenv
# load environment
load_dotenv(find_dotenv())


openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=256)
import requests
from pydantic import BaseModel, Field
import datetime


def code_generator(user_input):
    api_chain = APIChain.from_llm_and_api_docs(openai_llm, open_meteo_docs.OPEN_METEO_DOCS,
    verbose = True,
    limit_to_domains=["https://api.open-meteo.com/"]
    )
    pal_chain = PALChain.from_math_prompt(llm= openai_llm, verbose = True)
    result = pal_chain.run(user_input)
    return result
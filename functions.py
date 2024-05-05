# import required libraries
from langchain.chains.router import MultiPromptChain
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.utils.math import cosine_similarity
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_react_agent
# from langchain_community.chat_models import ChatAnthropic
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI

import os
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv, find_dotenv
# load environment
load_dotenv(find_dotenv())


openai_api_key = os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0.4, model="gpt-3.5-turbo")

# simple function to write an email
def write_email(input):
    email_prompt_template = """write a reply to the below email.
    email: {input}"""
    prompt = ChatPromptTemplate.from_template(email_prompt_template)
    chain = prompt | llm
    response = chain.invoke({"user_input":input}).content
    return response

def router(user_input):
    physics_template = """You are a very smart physics professor. \
    You are great at answering questions about physics in a concise\
    and easy to understand manner. \
    When you don't know the answer to a question you admit\
    that you don't know.

    Here is a question:
    {user_input}"""


    math_template = """You are a very good mathematician. \
    You are great at answering math questions. \
    You are so good because you are able to break down \
    hard problems into their component parts, 
    answer the component parts, and then put them together\
    to answer the broader question.

    Here is a question:
    {user_input}"""

    history_template = """You are a very good historian. \
    You have an excellent knowledge of and understanding of people,\
    events and contexts from a range of historical periods. \
    You have the ability to think, reflect, debate, discuss and \
    evaluate the past. You have a respect for historical evidence\
    and the ability to make use of it to support your explanations \
    and judgements.

    Here is a question:
    {user_input}"""


    computerscience_template = """ You are a successful computer scientist.\
    You have a passion for creativity, collaboration,\
    forward-thinking, confidence, strong problem-solving capabilities,\
    understanding of theories and algorithms, and excellent communication \
    skills. You are great at answering coding questions. \
    You are so good because you know how to solve a problem by \
    describing the solution in imperative steps \
    that a machine can easily interpret and you know how to \
    choose a solution that has a good balance between \
    time complexity and space complexity. 

    Here is a question:
    {user_input}"""

    embeddings = OpenAIEmbeddings()
    prompt_templates = [physics_template, math_template, history_template, computerscience_template]
    prompt_embeddings = embeddings.embed_documents(prompt_templates)

    def prompt_router(input):
        query_embedding = embeddings.embed_query(input["user_input"])
        similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
        most_similar = prompt_templates[similarity.argmax()]
        print(f"Using {most_similar}")
        return PromptTemplate.from_template(most_similar)


    chain = (
        {"user_input": RunnablePassthrough()}
        | RunnableLambda(prompt_router)
        | llm
        | StrOutputParser()
    )

    
    return chain.invoke(user_input)


def code_generator(user_input):
    tools = [PythonREPLTool()]
    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    agent = create_openai_functions_agent(ChatOpenAI(temperature=0), tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    answer = agent_executor.invoke({"input": prompt}).content
    return answer
op = router(" how are you?")
print(op)
import asyncio

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

joke_chain = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话") | llm
poem_chain = ChatPromptTemplate.from_template("给我写一首关于{topic}的诗") | llm
# 并行链
parallel_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

# 打印调用链，用于调试
# parallel_chain.get_graph().print_ascii()

resp = parallel_chain.invoke({"topic": "程序员"})
print(resp)

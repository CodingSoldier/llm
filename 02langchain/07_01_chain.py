from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os

from dotenv import load_dotenv

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-v3",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    api_base=os.environ.get("OPENAI_API_BASE")
)

prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话，不要任何解释。")

# langchain的链式调用

# 提示词模板 | 大模型 | 输出解析
chain = prompt | llm | StrOutputParser()
res = chain.invoke({"topic": "狗"})
print(res)

# 使用pipe函数
# chain = prompt.pipe(llm).pipe(StrOutputParser())
# res = chain.invoke({"topic": "狗"})
# print(res)

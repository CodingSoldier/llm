import os
# 导入DeepSeek聊天模型
from langchain_deepseek import ChatDeepSeek
# 导入字符串输出解析器
from langchain_core.output_parsers import StrOutputParser
# 导入chain装饰器，用于创建自定义链
from langchain_core.runnables import chain
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-v3",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    api_base=os.environ.get("OPENAI_API_BASE")
)

prompt1 = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话")
prompt2 = ChatPromptTemplate.from_template("这个笑话的主题是什么：{joke}")

@chain
def custom_chain(text):
    prompt_val1 = prompt1.invoke({"topic": text})
    output1 = llm.invoke(prompt_val1)
    parsed_output1 = StrOutputParser().invoke(output1)
    chain2 = prompt2 | llm | StrOutputParser()
    return chain2.invoke({"joke": parsed_output1})

resp = custom_chain.invoke("熊")
print(resp)





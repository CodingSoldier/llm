# PromptTemple提示词模板
字符串模板
```
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("你是一个{name}，帮我起一个具有{county}特色的{sex}名字")
prompts = prompt.format(name="算命大师", county="法国", sex="女孩")
print(prompts)
```
对话提示词模板
```
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个起名大师，你的名字叫"),
    ("human", "你好{name},你感觉如何？"),
    ("ai", "你好！我状态非常好!"),
    ("human", "你叫什么名字呢?"),
    ("ai", "你好！我叫{name}"),
    ("human", "{user_input}"),
])

chats = chat_template.format_messages(name="陈大师", user_input="你的爸爸是谁？")
print(chats)
```
message组合模板
```
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

sy = SystemMessage(
    content = "你是一个起名大师",
    additional_kwargs = {"大师名字": "狗蛋"}
)
hu = HumanMessage(
    content="请问大师叫什么？"
)
ai = AIMessage(
    content="我叫你爹"
)
print([sy, hu, ai])
```

使用MMR来检索相关示例，以使示例尽量符合输入
```
#使用MMR来检索相关示例，以使示例尽量符合输入
# Use MMR to retrieve relevant examples to make the examples as close as possible to the input

import os
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import (
    MaxMarginalRelevanceExampleSelector,
)
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import OpenAIEmbeddings

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")

#假设已经有这么多的提示词示例组：
# Suppose there are so many prompt examples:
examples = [
    {"input":"happy","output":"sad"},
    {"input":"tall","output":"short"},
    {"input":"sunny","output":"gloomy"},
    {"input":"windy","output":"calm"},
    {"input":"高兴","output":"悲伤"}
]

#构造提示词模版
# Construct prompt template
example_prompt = PromptTemplate(
    input_variables=["input","output"],
    template="原词：{input}\n反义：{output}"
)


#调用MMR
# Call MMR
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    #传入示例组
    # Pass in the example group
    examples,
    #使用openai的嵌入来做相似性搜索
    # Use openai's embedding for similarity search
    OpenAIEmbeddings(openai_api_base=api_base,openai_api_key=api_key),
    #设置使用的向量数据库是什么
    # Set what vector database is used
    FAISS,
    #结果条数
    # Number of results
    k=2,
)

#使用小样本模版
mmr_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="给出每个输入词的反义词",
    suffix="原词：{adjective}\n反义：",
    input_variables=["adjective"]
)

print(mmr_prompt.format(adjective="难过"))
```
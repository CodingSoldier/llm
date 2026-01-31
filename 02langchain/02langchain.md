# langchain使用环境搭建
1、安装python 3.12.1

2、打开vs code，创建02langchain目录

## 安装python虚拟环境

3、在02langchain目录下运行 python -m venv .venv 创建虚拟环境.venv

4、powershell执行 .\.venv\Scripts\Activate.ps1 进入.venv虚拟环境。cmd则是执行.\.venv\Scripts\activate.bat

## 安装jupyter

5、进入.venv虚拟环境后，运行 pip install jupyterlab  安装jupyterlab

6、运行 jupyter-lab 启动jupyter

7、在02langchain目录下创建01main.ipynb。在vs code中直接打开01main.ipynb 可以运行代码

## 配置.env文件

8、退出 jupyter-lab，在02langchain目录下新建.env配置文件

## 安装langchain

9、可以在01main.ipynb中运行 ! pip install langchain==0.3.18 安装langchain ，! 表示在命令行中安装。

10、01main.ipynb中运行 ! pip show langchain 显示乱码，可以在.venv虚拟环境或者浏览器的jupyter运行 pip show langchain 不会乱码，正常显示langchain版本

11、安装langchain-community，命令：! pip install -U langchain-community

## 使用langchain调用openai接口

12、申请openai的key很麻烦，使用https://sg.uiuiapi.com/register替代，邮箱tfz9011@163.com

13、在.env配置

OPENAI_API_KEY=sk-xxx

OPENAI_API_BASE=https://sg.uiuiapi.com/v1

14、在jupyter中运行代码，得到openai的回复
```
from langchain_openai import ChatOpenAI
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
llm.invoke("介绍下你自己")
```

使用PromptTemplate提示词模板
```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
prompt = PromptTemplate.from_template("你是一个起名大师，请模仿示例起3个{county}名字，比如：男孩经常被叫做{boy},女孩经常被叫做{girl}")
message=prompt.format(county="中国特色", boy="狗剩", girl="翠花")
print(message)

llm.invoke(message)
```

将字符串按逗号空格, 分割为字符串
```
from langchain_core.output_parsers import BaseOutputParser

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")
    
CommaSeparatedListOutputParser().parse("hi, bye")
```

使用逗号空格, 分割返回结果
```
from langchain_openai import ChatOpenAI  # 确保正确导入 ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import BaseOutputParser

# 自定义解析器
class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text):
        if hasattr(text, 'content'):
            text = text.content
        return text.strip().split(",")

# 加载环境变量
load_dotenv()
# 初始化 LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
 
# 创建提示模板
prompt = PromptTemplate.from_template(
    "你是一个起名大师，请模仿示例起3个{county}名字，比如：男孩经常被叫做{boy},女孩经常被叫做{girl}"
)
 
# 生成具体输入
message = prompt.format(
    county="中国特色",
    boy="狗剩",
    girl="翠花"
)
 
# 调用 LLM 并解析结果
response = llm.invoke(message)
parsed_result = CommaSeparatedListOutputParser().parse(response)
 
print("原始响应内容:", response.content)
print("解析后结果:", parsed_result)
```

# langchain核心组件ChatModels
## langchain模型组件标准参数介绍
### mmodel (str, 默认 "gpt-3.5-turbo")
指定使用的 OpenAI 模型名称，支持 gpt-3.5-turbo、gpt-4、gpt-4o 等。例如：

llm = ChatOpenAI(model="gpt-4-turbo")

### api_key (str, 可选)
OpenAI API 密钥，可通过环境变量 OPENAI_API_KEY 设置，或直接传入

llm = ChatOpenAI(api_key="sk-...")

### base_url (str, 可选)
自定义 API 地址，用于调用非官方 OpenAI 接口（如国内镜像服务）：

llm = ChatOpenAI(base_url="https://sg.uiuiapi.com/v1")

### temperature (float, 默认 0.7)
控制生成文本的随机性（0~2），值越低结果越确定，越高越创意：

llm = ChatOpenAI(temperature=0.3)  # 低随机性，适合事实性问答

### max_tokens (int, 可选)
限制生成文本的最大长度（token 数），避免过长输出：

llm = ChatOpenAI(max_tokens=200)  # 限制输出不超过200个token

### timeout (float, 可选)
请求超时时间（秒），避免长时间等待：

llm = ChatOpenAI(timeout=30)  # 30秒后超时

### stop (List[str], 可选)
指定停止词列表，模型遇到这些词会停止生成：

llm = ChatOpenAI(stop=["\n", "。"])  # 遇到换行或句号停止

### max_tokens (int, 可选)
限制生成文本的最大长度（token 数），避免过长输出：

llm = ChatOpenAI(max_tokens=200)  # 限制输出不超过200个token

## langchain一部分标准事件介绍
```
from langchain_openai import ChatOpenAI
import os
import asyncio

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
question="langchain是什么？"

# invoke事件，同步调用LLM处理单个输入，返回完整响应。
# llm.invoke(question)

# stream事件，同步流式返回LLM的响应块（tokens），支持实时输出。
# for chunk in llm.stream(question):
#     print(chunk.content + "|")

# batch 事件，批量处理多个输入，返回结果列表。
# llm.batch(["langchain作者是谁？", "langchain竞品有哪些？"])

# 异步事件流 astream_events。异步流式返回LLM执行过程中的事件（如开始、结束、中间步骤）。
async for event in llm.astream_events("介绍langchain", version="v2"):
    print(f"event={event['event']} | name={event['name']} | data={event['data']}")

```

利用Pydantic模型定义Joke的结构，通过LangChain的structured_output方法将大模型的输出结构化
```
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
    )

class Joke(BaseModel):
    """Joke to tell user."""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )
structured_llm = llm.with_structured_output(Joke, method="function_calling")
structured_llm.invoke("给我讲一个关于程序员的笑话")
```

使用TypedDict输出JSON数据

stream方法是异步输出
```
from typing_extensions import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from typing import Optional, Union
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
    )

class Joke(TypedDict):
    """Joke to tell user."""
    setup: Annotated[str, ..., "the setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

structured_llm = llm.with_structured_output(Joke, method="function_calling")
for chunk in structured_llm.stream("给我讲一个关于程序员的笑话"):
    print(chunk)
```

# 接入本地大模型
**ollama查看本地大模型列表**

ollama list

**安装本地大模型**

安装deepseek-r1:1.5b

llama run deepseek-r1:1.5b

安装llama2-chinese:7b

ollama run llama2-chinese:7b

**启动ollama**

ollama serve

**安装langchain-ollama**

使用ollama serve  启动ollama后，如何停止ollama服务

# 使用工具
让大模型使用工具。
```
#%%
import ChatOllama
from langchain_openai import ChatOpenAI
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
llm.invoke("介绍你自己")
#%%
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
prompt = PromptTemplate.from_template("你是一个起名大师，请模仿示例起3个{county}名字，比如：男孩经常被叫做{boy},女孩经常被叫做{girl}")
message=prompt.format(county="中国特色", boy="狗剩", girl="翠花")
print(message)

llm.invoke(message)
#%%
#起名大师，输出格式为一个数组
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
import os
from langchain_core.output_parsers import BaseOutputParser
from dotenv import load_dotenv

#自定义类
class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        if hasattr(text, 'content'):
            text = text.content
        t = text.strip().split(",")
        print(t)
        return t

load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
prompt = PromptTemplate.from_template("你是一个起名大师，请模仿示例起3个{county}名字，比如：男孩经常被叫做{boy},女孩经常被叫做{girl}")
message=prompt.format(county="中国广东特色", boy="狗剩", girl="翠花")
print(message)
strs = llm.invoke(message)
CommaSeparatedListOutputParser().parse(strs)
#%%
from langchain_openai import ChatOpenAI  # 确保正确导入 ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import BaseOutputParser

# 自定义解析器
class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text):
        if hasattr(text, 'content'):
            text = text.content
        return text.strip().split(",")

# 加载环境变量
load_dotenv()
# 初始化 LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url=os.getenv("OPENAI_API_BASE")
)
 
# 创建提示模板
prompt = PromptTemplate.from_template(
    "你是一个起名大师，请模仿示例起3个{county}名字，比如：男孩经常被叫做{boy},女孩经常被叫做{girl}"
)
 
# 生成具体输入
message = prompt.format(
    county="中国特色",
    boy="狗剩",
    girl="翠花"
)
 
# 调用 LLM 并解析结果
response = llm.invoke(message)
parsed_result = CommaSeparatedListOutputParser().parse(response)
 
print("原始响应内容:", response.content)
print("解析后结果:", parsed_result)
#%%
from langchain_openai import ChatOpenAI
import os
import asyncio

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
question="langchain是什么？"

# invoke事件，同步调用LLM处理单个输入，返回完整响应。
# llm.invoke(question)

# stream事件，同步流式返回LLM的响应块（tokens），支持实时输出。
# for chunk in llm.stream(question):
#     print(chunk.content + "|")

# batch 事件，批量处理多个输入，返回结果列表。
# llm.batch(["langchain作者是谁？", "langchain竞品有哪些？"])

# 异步事件流 astream_events。异步流式返回LLM执行过程中的事件（如开始、结束、中间步骤）。
async for event in llm.astream_events("介绍langchain", version="v2"):
    print(f"event={event['event']} | name={event['name']} | data={event['data']}")


#%%
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
    )

class Joke(BaseModel):
    """Joke to tell user."""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )
structured_llm = llm.with_structured_output(Joke, method="function_calling")
structured_llm.invoke("给我讲一个关于程序员的笑话")
#%%
from typing_extensions import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from typing import Optional, Union
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
    )

class Joke(TypedDict):
    """Joke to tell user."""
    setup: Annotated[str, ..., "the setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

structured_llm = llm.with_structured_output(Joke, method="function_calling")
for chunk in structured_llm.stream("给我讲一个关于程序员的笑话"):
    print(chunk)



#%%
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_anthropic import ChatAnthropic
import time
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

rate_limiter = InMemoryRateLimiter(
    requests_per_second=1,  # 每1秒请求一次
    check_every_n_seconds=0.1,  # 每100毫秒检查一次是否允许
    max_bucket_size=10,  # 控制最大突发大小
)
#定义模型调用
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
rate_limiter=rate_limiter #请求速率限制
)
#使用计时器来计算
# 每次请求的时间间隔
for _ in range(5):
    tic = time.time()
    model.invoke("hello")
    toc = time.time()
    print(toc - tic)
#%%
from typing_extensions import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from typing import Optional, Union
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
    )

class Joke(TypedDict):
    """Joke to tell user."""
    setup: Annotated[str, ..., "the setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

structured_llm = llm.with_structured_output(Joke, method="function_calling")
for chunk in structured_llm.stream("给我讲一个关于设计师的笑话"):
    print(chunk)
#%% sql

#%%
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os

class add(BaseModel):
    """Add two integers."""
    a: int = Field(..., description="The first integer")
    b: int = Field(..., description="The second integer")

class multiply(BaseModel):
    """Multiply two integers."""
    a: int = Field(..., description="The first integer")
    b: int = Field(..., description="The second integer")

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
tools = [add, multiply]
# 绑定工具
llm_with_tools = llm.bind_tools(tools);
query="3乘以12是多少？"
# 大模型处理“3乘以12”的时候调用了multiply类
llm_with_tools.invoke(query).tool_calls
```



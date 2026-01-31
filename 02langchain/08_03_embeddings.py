import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_community.document_loaders import PyPDFLoader
import base64
import io
from IPython.display import Image as IPImage
from IPython.display import display
from langchain_core.messages import HumanMessage
import fitz
from PIL import Image
from langchain_openai import ChatOpenAI
import os
from langchain_openai import OpenAIEmbeddings
load_dotenv()

# 使用openAI的嵌入模型
# embeddings_model = OpenAIEmbeddings()

# 使用siliconflow的代理
# https://cloud.siliconflow.cn/me/models
embeddings_model = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    api_key=os.environ.get("SILICONFLOW_API_KEY"),
    base_url=os.environ.get("SILICONFLOW_API_BASE")
)

embeddings = embeddings_model.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ]
)

print(len(embeddings))
print(len(embeddings[0]))

query_embeddings = embeddings_model.embed_query("What's the meaning of life?")
print(query_embeddings)






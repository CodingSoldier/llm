import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_community.document_loaders import PyPDFLoader


load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-v3",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    api_base=os.environ.get("OPENAI_API_BASE")
)

'''
安装依赖
pip install langchain_community
pip install pypdf
'''

# 加载08/deepseek.pdf
file_path = "08/deepseek.pdf"
loader = PyPDFLoader(file_path)
pages = loader.load()

print(f"{pages[0].metadata}\n")
print(pages[0].page_content)


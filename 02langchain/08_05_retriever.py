from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import os

from dotenv import load_dotenv

load_dotenv()

loader = TextLoader("./08/test.txt", encoding="utf-8")
# 加载文件内容为Document对象列表
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# 分割成1000字符/块，无重叠
texts = text_splitter.split_documents(documents)

# 初始化嵌入模型
embeddings = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    api_key=os.environ.get("SILICONFLOW_API_KEY"),
    base_url=os.environ.get("SILICONFLOW_API_BASE")
)
# 创建向量数据库
vectorstore = FAISS.from_documents(texts, embeddings)
# 创建检索器
retriever = vectorstore.as_retriever()

docs = retriever.invoke("deepseek是什么？")
print(docs)



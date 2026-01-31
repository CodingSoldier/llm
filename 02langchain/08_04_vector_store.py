
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv

load_dotenv()

embeddings_model = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    api_key=os.environ.get("SILICONFLOW_API_KEY"),
    base_url=os.environ.get("SILICONFLOW_API_BASE")
)

# 使用内存向量数据库
vector_store = InMemoryVectorStore(embedding=embeddings_model)

document_1 = Document(
    page_content="今天在抖音学会了一个新菜：锅巴土豆泥！看起来简单，实际炸了厨房，连猫都嫌弃地走开了。",
    metadata={"source": "社交媒体"}
)

document_2 = Document(
    page_content="小区遛狗大爷今日播报：广场舞大妈占领健身区，遛狗群众纷纷撤退。现场气氛诡异，BGM已循环播放《最炫民族风》两小时。",
    metadata={"source": "社区新闻"}
)

documents = [document_1, document_2]

# 添加文档
result_list = vector_store.add_documents(documents)
print(result_list)

# 添加文档和ID
vector_store.add_documents(documents=documents, ids=["doc1", "doc2"])

query = "遛狗"

# 相似度搜索
docs = vector_store.similarity_search(query)
print(docs[0].page_content)

# 向量搜索
embedding_vector = embeddings_model.embed_query(query)
docs = vector_store.similarity_search_by_vector(embedding_vector)
print(docs[0].page_content)

# 删除文档
vector_store.delete(ids=["doc1"])
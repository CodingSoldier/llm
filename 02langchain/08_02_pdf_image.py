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

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

'''
安装依赖
pip install PyMuPDF pillow langchain-openai IPython
'''

# 加载08/z2021.pdf
file_path='08/z2021.pdf'

def pdf_page_to_base64(pdf_path: str, page_number: int):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(page_number - 1)  # input is one-indexed
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")

base64_image = pdf_page_to_base64(file_path, 11)
display(IPImage(data=base64.b64decode(base64_image)))

# base64_image包含了"一线城市消费者占比有多少？"的答案
# 将问题和图片传给大模型，让大模型从图片中找出答案
query = "一线城市消费者占比有多少？"
message = HumanMessage(
    content=[
        {"type": "text", "text": query},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        }
    ]
)

resp = llm.invoke([message])
print(resp)
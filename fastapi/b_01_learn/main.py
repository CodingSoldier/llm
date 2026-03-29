from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from a1_param.a1_params import a1

app = FastAPI()

# CORS
origins = [
    "http://localhost:9528",
    "http://127.0.0.1:9528",
    'http://192.168.0.66:9528/',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(a1)

# 把项目下的static目录作为静态文件的访问目录
# app.mount('/static', StaticFiles(directory='static'), name='my_static')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post('/test', tags=['给接口分组的标签'], summary='测试的接口', description='接口的详细描述', response_description='响应数据的详细描述')
def test():
    print('执行了test函数')
    return {'msg': 'OK!'}
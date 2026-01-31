from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from exception.exception_handler import regitster_exception_handler
from routers import news, users, favorite

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],     # 允许的请求方法
    allow_headers=["*"],     # 允许的请求头
)

# 注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)


# 全局异常处理
regitster_exception_handler(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}


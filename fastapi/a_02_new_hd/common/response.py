from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# 统一返回值
def success_response(message: str = "success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    # JSONResponse 是一个用于创建返回 JSON 格式数据的响应对象，在 Web 框架（如 FastAPI）中经常被使用。
    # 主要特点
    # 返回 JSON 数据：将 Python 对象转换为 JSON 格式的 HTTP 响应
    # 设置响应头：自动设置 content-type: application/json
    # 支持状态码：可自定义 HTTP 状态码
    # 支持响应头：可添加自定义响应头
    return JSONResponse(content = jsonable_encoder(content))



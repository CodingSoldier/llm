# 导入DeepSeek聊天模型
# 导入字符串输出解析器
# 导入chain装饰器，用于创建自定义链
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_redis import RedisChatMessageHistory

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-v3",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY"),
    api_base=os.environ.get("OPENAI_API_BASE")
)

'''
启动redis-stack-server
docker run --name langchain-redis -d -p 6379:6379 \
  --privileged=true \
  redis/redis-stack-server \
  redis-server \
    --bind 0.0.0.0 \
    --protected-mode no \
    --save 60 1 \
    --loglevel warning \
    --loadmodule /opt/redis-stack/lib/rejson.so \
    --loadmodule /opt/redis-stack/lib/redisearch.so
'''
# 使用Redis存储历史记录
REDIS_URL = "redis://192.168.1.221:6379"
history = RedisChatMessageHistory(session_id="user_123", redis_url=REDIS_URL)

history.add_user_message("你好，AI助手！")
history.add_ai_message("你好！我今天能为你提供什么帮助？")
print("聊天历史：")
for message in history.messages:
    print(f"{type(message).__name__}: {message.content}")


from datetime import datetime

from fastapi import FastAPI, Path, Query, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

# 中间件（Middleware） 是一个在每次请求进入 FastAPI 应用时都会被执行的函数。
# 它在请求到达实际的路径操作（路由处理函数） 之前运行， 并且在响应返回给客户端之前再运行一次。
# 中间件： 函数的顶部使用装饰器 @app.middleware("http")

@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response

@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response

@app.get("/")
async def root():
    return {"message": "Hello World5555"}


@app.get("/hello")
async def get_hello():
    return {"msg": "你好"}

@app.get("/book_get_id/{id}")
async def get_book_get_id(id: int = Path(..., gt=0, lt=101, description="书籍id，取值范围1-100")):
    return {"id": id, "title": f"这是第{id}本书"}


# 需求：查找书籍的作者，路径参数 name，长度范围 2-10
@app.get("/author/{name}")
async def get_authorname(name: str = Path(..., min_length=2, max_length=10,
                                          description="作者姓名，长度范围2-10个字符")):
    return {"msg": f"这是{name}的信息"}

# ...表示必填
@app.get("/new_list")
async def get_new_list(
        skip: int = Query(..., description="跳过的记录数", lt=100),
        limit: int = Query(10, description="返回的记录数")
):
    return {"skip": skip, "limit": limit}



class User(BaseModel):
    username: str = Field(default="张三", min_length=2, max_length=10,
                          description="用户名，长度要求2-10个字")
    password: str = Field(min_length=3, max_length=20)

@app.post("/register")
async def register(user: User):
    return user


@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>标题一</h1>"

@app.get("/files")
async def get_files():
    return FileResponse("./files/1.jpeg")


class New(BaseModel):
    id: int
    title: str
    content: str

@app.get("/new/{id}", response_model=New)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是第{id}本书",
        "content": "书的内容"
    }


@app.get("/new/ex/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3]
    if id not in id_list:
        raise HTTPException(status_code=400, detail="您查找的新闻不存在")
    return {
        "id": id,
        "title": f"这是第{id}本书",
        "content": "书的内容"
    }

# 依赖注入
# 1、定义依赖项
async def common_parameters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=60)
):
    return {"skip": skip, "limit": limit}

# 2、声明依赖项
@app.get("/news/new_list")
async def get_news_list(commons=Depends(common_parameters)):
    return commons


# ORM
# 安装 pip install sqlalchemy[asyncio] aiomysql

# 1、创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/cpq?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, # 可选，输出 SQL 日志
    pool_size=10, # 设置连接池活跃的连接数
    max_overflow=20 # 允许额外的连接数
)

# 2、定义模型基类
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now(), comment="修改时间")

# 3、继承模型基类，创建表实体类
class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")

# 4、定义函数建表 ——> FastAPI启动的时候调用建表函数
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 5、系统启动时建表
@app.on_event("startup")
async def startup_event():
    await create_tables()




# 需求：查询功能的接口，查询图书
# 依赖注入：创建依赖项获取数据库会话 + Depends注入路由处理函数
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)

# 依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 有异常，回滚
            raise
        finally:
            await session.close()  # 关闭会话

@app.get("/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    # 查询
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book

@app.get("/books/get")
async def get_book_get(db: AsyncSession = Depends(get_database)):
    # 根据主键查询
    book = await db.get(Book, 1)
    return book

@app.get("/books/get_id/{book_id}")
async def books_get_id(book_id: int, db: AsyncSession=Depends(get_database)):
    # result = await db.execute(select(Book).where(Book.id==book_id))
    # book = result.scalar_one_or_none()

    result = await db.execute(select(Book).where(Book.id >= book_id))
    book = result.scalars().all()
    return book


@app.get("/books/search_book")
async def get_search_book(db: AsyncSession = Depends(get_database)):
    # like条件
    # result = await db.execute(select(Book).where(Book.author.like("更更%")))

    # & | ~ 与非
    # result = await db.execute(select(Book)
    #                           .where((Book.author.like("更更%")) | (Book.price > 10)))

    # in_()
    id_list = [2, 3]
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))
    book = result.scalars().all()
    return book

@app.get("/books/sum")
async def get_sum(db: AsyncSession = Depends(get_database)):
    # 聚合查询 select( func.方法名(模型类.属性) )
    # result = await db.execute(select(func.count(Book.id)))
    # result = await db.execute(select(func.sum(Book.price)))
    result = await db.execute(select(func.max(Book.price)))
    num = result.scalar()  # 用来提取一个数值 → 标量值
    return num

@app.get("/books/get_book_list")
async def get_book_list(
    page: int = 1,
    page_size: int = 3,
    db: AsyncSession = Depends(get_database)
):
    # （页码 - 1） * 每页数量
    skip = (page - 1) * page_size

    # offset 跳过的记录数  ； limit 每页的记录数
    stmt = select(Book).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books




class BookAdd(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

@app.post("/book/add")
async def book_add(book: BookAdd, db: AsyncSession = Depends(get_database)):
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book




class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int,
        data: BookUpdate,
        db: AsyncSession = Depends(get_database)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")
    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher
    await db.commit()
    return db_book




@app.delete("/book/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    # 先查再删 提交
    db_book = await db.get(Book, book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="查无此书"
        )

    await db.delete(db_book)
    await db.commit()
    return {"msg": "删除图书成功"}

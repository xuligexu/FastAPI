"""
    ORM: 对象关系映射

    ORM 建表:
        1. 创建异步引擎: "mysql+aiomysql://数据库用户名:数据库密码@localhost:端口号/数据库名?charset=utf8"
        2. 定义模型类
        3. 启动应用时建表

"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import String, Float

from datetime import datetime

from sqlalchemy import DateTime, func

import uvicorn



# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://dev_user:123456@localhost:3306/FastAPI_first?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 可选，输出 SQL 日志
    pool_size=10, # 设置连接池活跃的连接数
    max_overflow=20 # 允许额外的连接数
)
    

# 2. 定义模型类: 基类 + 表对应的模型类
# 基类: 创建时间、更新时间; 书籍表: id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    create_time: Mapped[datetime]=mapped_column(
        DateTime, 
        insert_default=func.now(),
        comment="创建时间"
    )

    update_time: Mapped[datetime]=mapped_column(
        DateTime, 
        insert_default=func.now(),
        onupdate=func.now(), 
        comment="修改时间"
    )



class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        comment = "书籍id"
    )
    bookname: Mapped[str] = mapped_column(
        String(255),
        comment = "书名"
    )
    author: Mapped[str] = mapped_column(
        String(255), 
        comment="作者"
    )
    price: Mapped[float] = mapped_column(
        Float,
        comment="价格"
    )
    publisher: Mapped[str] = mapped_column(
        String(255), 
        comment="出版社"
    )



# 3. 建表: 定义函数建表 -> FastAPI 启动德时候调用建表的函数
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
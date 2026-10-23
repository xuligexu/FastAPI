"""
    ORM 操作数据-改
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy import DateTime, func,String, Float

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import BaseModel

import uvicorn


# 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://dev_user:123456@localhost:3306/FastAPI_first?charset=utf8"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    max_overflow=20,
    pool_size=10
)


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        comment="创建时间"
    )

    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        onupdate=func.now(),
        comment="修改时间"
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int]=mapped_column(
        primary_key=True,
        comment="书籍id"
    )

    bookname: Mapped[str]=mapped_column(
        String(255),
        comment="书名"
    )

    author: Mapped[str]=mapped_column(
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

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


#依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try: 
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()



# 需求: 修改图书信息: 先查再改
# 设计思路: 路径参数书籍id: 作用是查找; 请求体参数: 作用是新数据 (书名、作者、价格、出版社)

class Bookupdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str
@app.put("/book/update_book/{book_id}")
async def update_book(
    book_id: int,
    data: Bookupdate,
    db: AsyncSession = Depends(get_database)
):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="查无此书"
        )

    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher

    return db_book



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
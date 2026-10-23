"""
    ORM 操作数据: 增、删、改、查
"""

"""
    ORM 操作数据: 查
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime

from sqlalchemy import DateTime, func, select, String, Float

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


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)

# 依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session # 返回数据库会话给路由处理函数
            await session.commit() # 提交事务
        except Exception:
            await session.rollback() # 有异常，回滚
            raise
        finally:
            await session.close() # 关闭会话



@app.get("/book/books")
async def get_book_list(
    db: AsyncSession = Depends(get_database)
):
    # result = await db.execute(select(Book)) # 查询 -> 返回一个 ORM 对象
    # book = result.scalars().all()  # 获取所有

    # book = result.scalars().first() # 获取第一个

    book = await db.get(Book, 1) # 获取主键为""的单条

    return book



# -------------------------------------------
# where() 条件查询

# 需求: 路径参数 书籍id
@app.get("/book/get_book/{book_id}")
async def get_book_list(
    book_id: int,
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    return book

# 需求: 条件 价格大于等于200
@app.get("/book/search_book")
async def get_search_book(
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Book).where(Book.price >= 200))
    books = result.scalars().all()
    return books


# ---------------------------------------------
# like() 模糊查询 
# %: 零个、一个或多个字符
# _: 一个单个字符

@app.get("/book/find_book")
async def get_find_book(
    db: AsyncSession = Depends(get_database)
):
    # 需求: 作者以 曹 开头  % _ 
    # like() 模糊查询: % 任意个字符;  
    # _ 一个单个字符
    # result = await db.execute(select(Book).where(Book.author.like("曹_")))

    # & | ~ 与非
    # result = await db.execute(select(Book).where((Book.author.like("曹%")) | (Book.price > 100)))

    # in_() 包含
    # 需求: 书籍id 列表，数据库里面的 id 如果在 书籍id列表里面 就返回
    id_list = [1, 3, 5, 7]
    result = await db.execute(select(Book).where(Book.id.in_(id_list)))

    book = result.scalars().all()
    return book





#------------------------------------------------
# 聚合查询
@app.get("/book/count")
async def get_count(db: AsyncSession = Depends(get_database)):
    # result = await db.excute(select(func.count(Book.id)))
    # result = await db.execute(select(func.max(Book.price)))
    # result = await db.excute(select(func.sum(Book.price)))
    result = await db.excute(select(func.avg(Book.price)))
    count = result.scalar()
    return count


#------------------------------------------------
# 分页查询
@app.get("/book/get_book_list")
async def get_book_list(
    db: AsyncSession = Depends(get_database),
    page: int = 1,
    page_size: int = 3,
):
    skip = (page - 1) * page_size
    stmt = select(Book).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books


#------------------------------------------------


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
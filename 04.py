"""
    查询参数 Query() 与Path函数拥有的属性都适用
"""



from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}



# 查询新闻 -> 分页，skip: 跳过的记录数, limit: 返回的记录数 10
@app.get("/news/news_list")
async def get_news_list(
    skip: int = Query(0, description = "跳过的记录数", lt = 100), 
    limit: int = Query(10, description = "返回的记录数")
    ):
    return {"skip": skip, "limit": limit}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
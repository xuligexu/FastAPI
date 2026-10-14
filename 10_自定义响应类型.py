"""
    自定义响应数据格式
"""



from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# 创建 FastAPI 实例
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}

class News(BaseModel):
    id: int
    title: str
    content: str



@app.get("/news/{id}", response_model = News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是第{id}本书",
        "content": "这是一本好书"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

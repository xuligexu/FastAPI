"""
    参数分类：路径参数   查询参数   请求体
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 路径参数
@app.get("/book/{id}")
async def get_book(id: int):
    return {"id": id, "title": f"这是第{id}本书"}

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
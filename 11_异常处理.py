"""
    异常处理
    导入 HTTPException
"""

from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}

# 需求: 按 id 查询新闻 -> 1-6
@app.get("/news/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        # raise 抛出异常
        raise HTTPException(status_code = 404, detail = "您查找的信息不存在")
    return {"id": id}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
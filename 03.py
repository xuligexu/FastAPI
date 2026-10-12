"""
    路径参数 - 类型注解 
    Path: ...(必填), gt/ge(大于/大于等于), lt/le(小于/小于等于), description(描述), min_length/max_length(最小长度/最大长度)
"""

from fastapi import FastAPI, Path
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/book/{id}")
async def get_book(id: int = Path(..., gt = 0, le = 100, description = "书籍的id， 取值范围1-100")):
    return {"id": id, "title": f"这是第{id}本书"}

# 查找书籍的作者，路径参数 name，长度范围 2-10
@app.get("/author/{name}")
async def get_name(name: str = Path(..., min_length = 2, max_length = 10, description = "书籍的作者填写，长度 2-10")):
    return {"msg": f"这是{name}的信息"}


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
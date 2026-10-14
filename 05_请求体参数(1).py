"""
    请求体参数, 1.定义类型，2.类型注解
"""


from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}


# 注册：用户名和密码 -> str 
class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: User):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
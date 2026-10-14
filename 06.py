"""
    请求体参数类型注解, Field, 新增: default(默认值)
"""


from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}


# 注册：用户名和密码 -> str 
class User(BaseModel):
    username: str = Field(..., default = "yourname", min_length = 2, max_length = 10)
    password: str  = Field(..., min_length = 4, max_length = 10)

@app.post("/register")
async def register(user: User):
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
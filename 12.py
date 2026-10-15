"""
    fastapi 的中间件
    使用中间件为每个请求前后添加统一的处理逻辑
"""

from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}

# 中间件
@app.middleware("http")
async def middleware1(request, call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response


@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
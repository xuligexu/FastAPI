"""
    响应类型:
        fastapi 默认支持响应为json格式
        JSONResponse: 默认响应，返回JSON数据
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
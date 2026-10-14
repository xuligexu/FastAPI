"""
    HTMLResponse 返回 HTML 内容
    装饰器中指定相应类
"""


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 装饰器中指定响应类
@app.get("/html", response_class = HTMLResponse)
async def get_html():
    return "<h1>这是标题</h1>"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
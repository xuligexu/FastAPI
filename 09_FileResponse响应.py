"""
    FileResponse 返回文件下载
    返回响应对象
"""


from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 返回响应对象
#接口: 返回一张图片内容
@app.get("/file")
async def get_file():
    file_path = "./OIP-C.webp"
    return FileResponse(file_path)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
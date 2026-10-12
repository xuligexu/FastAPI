from fastapi import FastAPI
import uvicorn

# 创建 FastAPI 实例
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 可直接运行，也可在终端输入 : 
#   uvicorn "文件名":"应用实例名" --reload
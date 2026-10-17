"""
    依赖注入系统

    依赖注入系统的作用: 
        抽取可复用的组件，实现代码复用、解耦且可轻松替换依赖项进行测试

    使用依赖注入系统:
        创建依赖项 -> 导入Depends -> 声明依赖项
"""


from fastapi import FastAPI, Query, Depends # 2.导入Depends
import uvicorn


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World888"}



# 分页参数逻辑公用: 新闻列表和用户列表
# 1. 依赖项
async def common_parameters(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=60)
):
    return {
        "skip": skip,
        "limit": limit
    }



@app.get("/news/news_list")
async def get_news_list(
    # 3. 声明依赖项
    commons = Depends(common_parameters)
):
    return commons


@app.get("/user/user_list")
async def get_user_list(
    commons = Depends(common_parameters)
):
    return commons



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
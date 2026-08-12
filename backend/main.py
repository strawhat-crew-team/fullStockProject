from fastapi import FastAPI


app = FastAPI(title="tm 时间管理API", version="0.1.0")

@app.get("/")
async def index():
    return {"message": "后端服务已启动"}





# _*_ coding:utf-8 _*_
# @File  : main.py
# @Time  : 2020-07-18 18:38
# @Author: zizle
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from routers import router

app = FastAPI()

app.mount("/download-files/", StaticFiles(directory="F:/ADSCLIENTS/"), name="clientUpdate")


@app.get("/", tags=["主页"])
async def index():
    return HTTPException(status_code=404)
    # return {"message": "The Analysis Decision System 2.0 Service."}

app.include_router(router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

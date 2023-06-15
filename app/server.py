import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from loguru import logger

from exceptions import APPBaseException, ErrorCode
from util._queue import Concur_Wait_Time, taskqueue
from lib.api.callback import time_out
from task.bot._typing import CallbackData
import json

def init_app():
    _app = FastAPI(title="Midjourney API")
    scheduler = AsyncIOScheduler()

    register_blueprints(_app)
    exc_handler(_app)

    @scheduler.scheduled_job('interval', minutes=5)
    async def cron_job():
        # 执行任务的内容，例如打印当前时间
        for key in Concur_Wait_Time:
            logger.debug(f"当前任务{key}, 等待时间{(datetime.now() - Concur_Wait_Time[key]).seconds}")
            if (datetime.now() - Concur_Wait_Time[key]).seconds > 290:
                f = json.load(open("vip.json", "r"))
                taskqueue.pop(key)
                logger.debug(f"队列中剩余:{Concur_Wait_Time}")
                await time_out(CallbackData(
                    socketType=2,
                    list= [
                    {
                        "type":203,
                        "titleList":["xxxxxxxx"],
                        "receivedContent":"您的生成结果超时，请稍后再试",
                        "atList": [key],
                    },
                    ] if key not in f else[
                    {
                        "type":203,
                        "titleList":[key],
                        "receivedContent":"您的生成结果所需时间较长，将在稍后发送给您",
                        "atList": [key],
                    },                       
                    ]
                ))
                break

    
    # 启动scheduler
    @_app.on_event("startup")
    async def startup_event():
        logger.debug("FastApi服务启动")
        # 启动定时任务
        logger.debug("定时任务启动")
        scheduler.start()
    @_app.on_event("shutdown")
    async def shutdown_event():
        logger.debug("FastApi服务关闭")
        scheduler.shutdown()
        logger.debug("定时任务关闭")


    return _app


def exc_handler(_app):
    @_app.exception_handler(RequestValidationError)
    def validation_exception_handler(_, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": ErrorCode.REQUEST_PARAMS_ERROR.value,
                "message": f"request params error: {exc.body}"
            },
        )

    @_app.exception_handler(APPBaseException)
    def validation_exception_handler(_, exc: APPBaseException):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": exc.code.value,
                "message": exc.message
            },
        )


def register_blueprints(_app):
    from app import routers
    _app.include_router(routers.router, prefix="/v1/api/trigger")


def run(host, port):
    _app = init_app()
    uvicorn.run(_app, port=port, host=host)

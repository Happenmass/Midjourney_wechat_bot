debug = False
from fastapi import APIRouter, UploadFile

from lib.api import discord
from lib.api.discord import TriggerType
from util._queue import taskqueue
from .handler import prompt_handler, unique_id, check_command
from exceptions import BannedPromptError, CommandError
from .schema import (
    TriggerImagineIn,
    TriggerUVIn,
    TriggerResetIn,
    QueueReleaseIn,
    TriggerResponse,
    UploadResponse,
    TriggerDescribeIn,
    SendMessageResponse,
    SendMessageIn,
)
import json

router = APIRouter()


@router.post("/imagine", response_model=TriggerResponse)
async def imagine(body: TriggerImagineIn):
    trigger_id = body.receivedName
    vip = json.load(open("vip.json", "r"))
    if(not body.atMe):
        if (trigger_id not in vip):
            return {"data": {
                "type": 0,
                "info": {
                    "text": "请直接告诉我您想生成的内容"
                }
            }}
        # else :
        #     return {"data": {
        #         "type": 0,
        #         "info": {
        #             "text": "请直接告诉我您想生成的内容～"
        #         }
        #     }}
    try:
        f = json.load(open("cetification.json", "r"))
        limits = f[trigger_id]['limits']
        if (limits < 1):
            return {"data": {
                "type": 0,
                "info": {
                    "text": "对不起，您今日的试用次数已用完"
                }
            }}
    except KeyError:
        return {"data": {
            "type": 0,
            "info": {
                "text": "您还没有使用权限，请联系客服添加"
            }
        }}
    f2 = json.load(open("status.json", "r"))
    with open("status.json", "w") as file:
        if body.spoken == "U1":
            try:
                f2[trigger_id]["last_type"] = "U"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.upscale, **{
                "index": 1,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成高清大图,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "U2":
            try:
                f2[trigger_id]["last_type"] = "U"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.upscale, **{
                "index": 2,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成高清大图,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "U3":
            try:
                f2[trigger_id]["last_type"] = "U"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.upscale, **{
                "index": 3,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成高清大图,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "U4":
            try:
                f2[trigger_id]["last_type"] = "U"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.upscale, **{
                "index": 4,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成高清大图,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "V1":
            try:
                f2[trigger_id]["last_type"] = "V"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.variation, **{
                "index": 1,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成相似图像,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "V2":
            try:
                f2[trigger_id]["last_type"] = "V"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.variation, **{
                "index": 2,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成相似图像,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "V3":
            try:
                f2[trigger_id]["last_type"] = "V"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.variation, **{
                "index": 3,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成相似图像,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        if body.spoken == "V4":
            try:
                f2[trigger_id]["last_type"] = "V"
                json.dump(f2, file)
                trigger_type = TriggerType.upscale.value
                taskqueue.put(trigger_id, discord.variation, **{
                "index": 4,
                "msg_id": f[trigger_id]["last_message_id"],
                "msg_hash": f[trigger_id]["last_meassage_hash"],
                "trigger_id": trigger_id
                })
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "正在为您生成相似图像,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
                    }
                }}
            except:
                return {"data": {
                    "type": 0,
                    "info": {
                        "text": "指令错误，请重新输入"
                    }
                }}
        try:
            prompt = prompt_handler(body.spoken, body.receivedName, body.picurl)[1]
        except BannedPromptError:
            json.dump(f2, file)
            file.close()
            return {"data": {
                "type": 0,
                "info": {
                    "text": "检测到违禁词，请重新输入"
                }
            }}
        try:
            check_command(prompt)
        except CommandError:
            json.dump(f2, file)
            file.close()
            return {"data": {
                "type": 0,
                "info": {
                    "text": "指令错误，请使用'--'"
                }
            }}
        print("recieve imagine request from"+body.receivedName+"in the group"+body.groupName)
        print(prompt)
        trigger_type = TriggerType.generate.value
        ret =  taskqueue.put(trigger_id, discord.generate, prompt)
        f2[trigger_id]["last_type"] = "G"
        json.dump(f2, file)
        if(ret != None):
            return ret
        return {"data": {
        "type": 0,
        "info": {
            "text": "(debug 模式)成功提交任务，请耐心等待, 文本翻译为"+prompt if debug else "成功提交任务,您当前排在第"+str(len(taskqueue._wait_queue)+len(taskqueue._concur_queue))+"位,今日剩余次数"+str(limits-1)+"次,请耐心等待"
        }
    }}


# @router.post("/upscale", response_model=TriggerResponse)
# async def upscale(body: TriggerUVIn):
#     trigger_id = body.trigger_id
#     trigger_type = TriggerType.upscale.value

#     taskqueue.put(trigger_id, discord.upscale, **body.dict())
#     return {"trigger_id": trigger_id, "trigger_type": trigger_type}


# @router.post("/variation", response_model=TriggerResponse)
# async def variation(body: TriggerUVIn):
#     trigger_id = body.trigger_id
#     trigger_type = TriggerType.variation.value

#     taskqueue.put(trigger_id, discord.variation, **body.dict())
#     return {"trigger_id": trigger_id, "trigger_type": trigger_type}


# @router.post("/reset", response_model=TriggerResponse)
# async def reset(body: TriggerResetIn):
#     trigger_id = body.trigger_id
#     trigger_type = TriggerType.reset.value

#     taskqueue.put(trigger_id, discord.reset, **body.dict())
#     return {"trigger_id": trigger_id, "trigger_type": trigger_type}


# @router.post("/describe", response_model=TriggerResponse)
# async def describe(body: TriggerDescribeIn):
#     trigger_id = body.trigger_id
#     trigger_type = TriggerType.describe.value

#     taskqueue.put(trigger_id, discord.describe, **body.dict())
#     return {"trigger_id": trigger_id, "trigger_type": trigger_type}


# @router.post("/upload", response_model=UploadResponse)
# async def upload_attachment(file: UploadFile):
#     if not file.content_type.startswith("image/"):
#         return {"message": "must image"}

#     trigger_id = str(unique_id())
#     filename = f"{trigger_id}.jpg"
#     file_size = file.size
#     attachment = await discord.upload_attachment(filename, file_size, await file.read())
#     if not (attachment and attachment.get("upload_url")):
#         return {"message": "Failed to upload image"}

#     return {
#         "upload_filename": attachment.get("upload_filename"),
#         "upload_url": attachment.get("upload_url"),
#         "trigger_id": trigger_id,
#     }


# @router.post("/message", response_model=SendMessageResponse)
# async def send_message(body: SendMessageIn):
#     picurl = await discord.send_attachment_message(body.upload_filename)
#     if not picurl:
#         return {"message": "Failed to send message"}

#     return {"picurl": picurl}


@router.post("/queue/release", response_model=TriggerResponse)
async def queue_release(body: QueueReleaseIn):
    """bot 清除队列任务"""
    try:
        taskqueue.pop(body.trigger_id)
    except:
        print("no trigger id need to be pop")
    return body

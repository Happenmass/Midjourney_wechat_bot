import asyncio
import re
from typing import Dict, Union, Any
import hashlib
import time

from discord import Message
from loguru import logger

from app.handler import PROMPT_PREFIX, PROMPT_SUFFIX
from lib.api.callback import queue_release, callback
from util.fetch import fetch
from task.bot._typing import CallbackData, Attachment, Embed
import requests
from retrying import retry
from PIL import Image
from PIL import PngImagePlugin
from io import BytesIO
from lib.api import IMG_BED_URL

from requests_toolbelt import MultipartEncoder
import json

TRIGGER_ID_PATTERN = f"{PROMPT_PREFIX}(.*?){PROMPT_SUFFIX}"  # 消息 ID 正则
PROMPT_PATTERN = "#>(.*?)"+re.escape('**')  # 消息正则
TEMP_MAP: Dict[str, bool] = {}  # 临时存储消息流转信息


def get_temp(trigger_id: str):
    return TEMP_MAP.get(trigger_id)


def set_temp(trigger_id: str):
    TEMP_MAP[trigger_id] = True


def pop_temp(trigger_id: str):
    asyncio.get_event_loop().create_task(queue_release(trigger_id))
    try:
        TEMP_MAP.pop(trigger_id)
    except KeyError:
        pass

def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10**10

def extract_prompt(message: Message) -> Union[str, None]:
    content = message.content
    match = re.findall(PROMPT_PATTERN, content)
    return match[0] if match else None

@retry(stop_max_attempt_number=3)
def post_img_to_imgbed(header, file):
    resp = requests.post(IMG_BED_URL+"/upload",headers = header, files=file)
    assert resp.status_code == 200  # 
    return resp

def extract_url(message: Message, trigger_id:str, vip_list) -> Union[str,None]:
    id = message.id
    ms_hash = message.attachments[0].filename.split("_")[-1].split(".")[0]
    # logger.debug(f"message.conteng{message.content}")
    f = json.load(open("cetification.json", "r"))
    f2 = json.load(open("status.json", "r"))
    limits = f[trigger_id]['limits']
    with open("cetification.json", "w") as file:
        try:
            if trigger_id not in vip_list:
                f[trigger_id]['limits'] = limits-1
            if(f2[trigger_id]["last_type"] != "U"):
                f[trigger_id]['last_message_id'] = str(id)
                f[trigger_id]['last_meassage_hash'] = str(ms_hash)
            file.write(json.dumps(f))
        except:
            file.write(json.dumps(f))
    attachment = message.attachments[0]
    Attachment(**attachment.to_dict())
    prompt = extract_prompt(message)
    # logger.debug(f"discord attachment: {attachment.url}")
    # logger.debug(f"prompt: {prompt}")
    img_data = requests.get(attachment.url)
    
    id = unique_id()
    tempIm = BytesIO(img_data.content)
    im = Image.open(tempIm)
    info = PngImagePlugin.PngInfo()
    info.add_text("prompt",prompt)
    im = im.resize((int(im.width*0.78),int(im.height*0.78)))
    im.save("img/"+str(id)+".png", optimize=True, pnginfo=info)

    # with open("img/"+prompt+str(id)+".png","wb+") as f:
    #     f.write(img_data.content)
    with open("img/"+str(id)+".png","rb") as f:
        header = {
                # "Content-Type": "multipart/form-data;boundary=ebf9f03029db4c2799ae16b5428b06bd1",
                "Accept": "application/json",
                "Authorization": "Bearer 3|0RQYNi3ujjrj3nRjlE6jnRQd4mlRTKdWru7NB0KP"}
        file = {"file": f}
        # form_data = MultipartEncoder(files)  # 格式转换
        
        resp = post_img_to_imgbed(header, file)
        logger.debug(f"response from Image Bed: {resp}")
        logger.debug(f"response from Image Bed: {resp.json()}")
    return resp.json()["data"]["links"]["url"]

# def extract_url(message: Message) -> str:
#     attachment = message.attachments[0]
#     Attachment(**attachment.to_dict())
#     print(attachment.proxy_url)
#     url = ""

#     return attachment.proxy_url

def match_trigger_id(content: str) -> Union[str, None]:
    match = re.findall(TRIGGER_ID_PATTERN, content)
    return match[0] if match else None


async def callback_trigger(trigger_id: str, trigger_status: str, message: Message):
    f = json.load(open("vip.json", "r"))
    await callback(CallbackData(
        socketType=2,
        list= [
        {
        "type": 218,
        "titleList":["xxxxxxxx"],
        "objectName":str(time.time()) + "GenerativeImage.png",
        # "fileUrl": "https://cdn.asrtts.cn/static/image/logo3_180_raw.png",
        "fileUrl": extract_url(message, trigger_id, f),
        "fileType": "image"
        },
        {
            "type":203,
            "titleList":["xxxxxxxx"],
            "receivedContent":"亲，请查收您的生成结果",
            "atList": [trigger_id],
        },
        ] if trigger_id not in f else [
        {
            "type": 218,
            "titleList":[trigger_id],
            "objectName":str(time.time()) + "GenerativeImage.png",
            # "fileUrl": "https://cdn.asrtts.cn/static/image/logo3_180_raw.png",
            "fileUrl": extract_url(message, trigger_id, f),
            "fileType": "image"
        },
        ]
    ))
    # await callback(CallbackData(
    #     type=trigger_status,
    #     id=message.id,
    #     content=message.content,
    #     attachments=[
    #         Attachment(**attachment.to_dict())
    #         for attachment in message.attachments
    #     ],
    #     embeds=[],
    #     trigger_id=trigger_id,
    # ))


async def callback_describe(trigger_status: str, message: Message, embed: Dict[str, Any]):
    url = embed.get("image", {}).get("url")
    trigger_id = url.split("/")[-1].split(".")[0]

    await callback(CallbackData(
        type=trigger_status,
        id=message.id,
        content=message.content,
        attachments=[],
        embeds=[
            Embed(**embed)
        ],
        trigger_id=trigger_id,
    ))
    return trigger_id

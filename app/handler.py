import hashlib
import time
from functools import wraps
from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse

from exceptions import BannedPromptError, CommandError
from lib.prompt import BANNED_PROMPT
import deepl
from lib.api import DEEPL_API_KEY
PROMPT_PREFIX = "<#"
PROMPT_SUFFIX = "#>"


def check_banned(prompt: str) -> None:
    is_banned = False
    # for w in BANNED_PROMPT:
    #     if (prompt.lower().find(w) != -1):
    #         is_banned = True
    #         print("违禁词："+ w)
    # if is_banned:
    #     raise BannedPromptError(f"banned prompt: {prompt}")
    words = set(w.lower().replace(',','').replace(' ','') for w in prompt.split())
    print(words)
    if len(words & BANNED_PROMPT) != 0:
        raise BannedPromptError(f"banned prompt: {prompt}")


def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10**10

def translate_api(prompt: str) -> str:
    """将中文字符串翻译为英文"""
    auth_key = DEEPL_API_KEY  # use DeepL free API 
    target_language = 'EN-US'      #"EN-US"
    #调用deepl
    translator = deepl.Translator(auth_key)  #input the auth_key
    #print(time.time())

    result = translator.translate_text(prompt,target_lang=target_language)
    return result.text


def prompt_handler(prompt: str, trigger_id: str, picurl: Union[str, None] = None):
    """
    拼接 Prompt 形如: <#1234567890#>a cute cat
    """
    prompt = translate_api(prompt)
    print(prompt)
    check_banned(prompt)

    # trigger_id = str(unique_id())

    if not picurl and prompt.startswith(("http://", "https://")):
        picurl, _, prompt = prompt.partition(" ")

    return trigger_id, f"{picurl+' ' if picurl else ''}{PROMPT_PREFIX}{trigger_id}{PROMPT_SUFFIX}{prompt}"
    # return f"{picurl+' ' if picurl else ''}{PROMPT_PREFIX}{trigger_id}{PROMPT_SUFFIX}{prompt}"

def check_command(command:str):
    if(('-ar' in command) and ('--ar' not in command)):
        raise CommandError(f"指令错误")
    if(('-s' in command) and ('--s' not in command)):
        raise CommandError(f"指令错误")
    if(('-niji' in command) and ('--niji' not in command)):
        raise CommandError(f"指令错误")
    if(('-v' in command) and ('--v' not in command)):
        raise CommandError(f"指令错误")
    if('--S' in command):
        raise CommandError(f"指令错误")
    if('--AR' in command):
        raise CommandError(f"指令错误")

def http_response(func):
    @wraps(func)
    async def router(*args, **kwargs):
        trigger_id, resp = await func(*args, **kwargs)
        if resp is not None:
            code, trigger_result = status.HTTP_200_OK, "success"
        else:
            code, trigger_result = status.HTTP_400_BAD_REQUEST, "fail"

        return JSONResponse(
            status_code=code,
            content={"trigger_id": trigger_id, "trigger_result": trigger_result}
        )

    return router

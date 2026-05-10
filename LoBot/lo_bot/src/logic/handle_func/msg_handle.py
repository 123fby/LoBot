from pathlib import Path
import json
import tiktoken
from typing import Dict,Any,List
import re  
from loguru import logger
from lo_bot.shared import load_config
TAG_SCHEMA={
    "reply":{
        "required":False,
    }, 
    "text":{
        "required":False
    },
    "emoji":{
        "required":False
    },
    "image":{
        "required":False
    },
    "tool":{
        "required":False
    },
    "video":{
        "required":False
    },
    "plugin":{
        "required":False
    },
    "memory":{
        "required":False
    },
    "weight":{
        "required":False
    },
}

async def load_whitelist():
    """
    加载白名单
    """
    list= load_config("lo_bot/config/whitelist.toml",private_withelist=[],group_withelist=[])
    return list
# def validate_tags(parsed):
#     for tag,config in TAG_SCHEMA.items():
#         if config.get("required") and tag not in parsed:
#             """.get()安全取值,parse 解析好的数据"""
#             return False
#         return True
async def assemble_memory(msg_info,ai_msg):
    """
    组装记忆
    """
async def msg_limit(msgs:list[Dict],max_tokens:int=4096,model:str="gpt-3.5-turbo"):
    """
    消息长度限制
    """
    
    encoding=tiktoken.encoding_for_model(model)
    token_counts=[]
    for msg in msgs:
        temp=json.dumps(msg,ensure_ascii=False, separators=(',', ':'))
        token_count=len(encoding.encode(temp))
        token_counts.append(token_count)
    total_tokens=sum(token_counts)
    index=0

    while total_tokens>max_tokens and index<len(msgs):
        total_tokens-=token_counts[index]
        index+=1
    msgs[:]=msgs[index:]#修改原列表，保留最后的消息(切片原地赋值)
async def __msg_extract(msgs,tag)->str:
    """
    提取消息
    """
    if msgs:
        result=re.search(rf"<{tag}>(.*?)</{tag}>",msgs,re.S|re.I)
        return result.group(1).strip() if result else None
    else:
        return None
    
async def msg_extract(msgs,TAG_SCHEMA:Dict[str,Any]=TAG_SCHEMA)->dict:
    """
    提取消息
    """
    tag_list=list(TAG_SCHEMA.keys())[1:]
    extract_msg=await __msg_extract(msgs,"reply")
    plain_msg=[]
    ability_msg={}
    for tag in tag_list:
        if tag not in extract_msg:
            continue
        plain=await __msg_extract(extract_msg,tag)
        if tag in ["tool","plugin","memory"] :
            temp=list(plain.split(",")) if plain else None
            ability_msg[tag]=temp
        elif tag=="weight":
            weight=int(plain)
        else:
            plain_msg.append(plain)
    logger.info(f"提取消息: {plain_msg}")
    return {"plain_msg": plain_msg, "ability": ability_msg, "weight": weight}

async def msg_filter(msg_info:Dict,whitelist)->bool:
    """
    消息过滤
    """
    if msg_info["scene_type"]=="private":
        if msg_info["user_id"] not in whitelist["private_whitelist"]:
            return False
    elif msg_info["scene_type"]=="group":
        if msg_info["group_id"] not in whitelist["group_whitelist"]:
            return False
    return True



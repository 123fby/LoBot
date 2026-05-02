"""
事件解析器
"""
from loguru import logger
from typing import Dict,Any,List
from nonebot.adapters.onebot.v11 import MessageEvent
async def msg_parser(event:MessageEvent)->Dict[str,Any]:
    """
    解析消息事件
    """
    user_id=str(event.user_id)
    message=event.get_message()
    msg=message.extract_plain_text().strip()
    nickname=getattr(event.sender,"nickname",None) or "未知用户"
    msg_type=event.message_type
    text_parts: List[str]=[]
    img_urls: List[str]=[]

    """
    解析图片消息
    预留位置
    """
    if msg_type=="group":
        scene_type="group"
        group_id=str(event.group_id)
    elif msg_type=="private":
        scene_type="private"
        group_id=None
    return {
        "user_id":user_id,
        "msg":msg,
        "nickname":nickname,
        "scene_type":scene_type,
        "group_id":group_id,
    }
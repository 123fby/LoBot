"""全局单例,用于存储全局变量,后续用fastapi的生命周期和依赖注入来管理全局变量,
该文件为临时文件，后续会移除"""
from lo_bot.src.logic.chat_flow import ChatFlow
_chat_flow: ChatFlow|None =None

def set_chat_flow(cf: ChatFlow):
    global _chat_flow
    if _chat_flow is None:
        _chat_flow=cf
def get_chat_flow():
    if _chat_flow is None:
        raise ValueError("chat_flow未初始化")
    return _chat_flow

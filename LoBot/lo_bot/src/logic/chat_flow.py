
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from loguru import logger
from typing import Dict,Any,List
from lo_bot.src.core.llm.llm_client import LLMClient
from lo_bot.src.core.memory.memory_manager import MemoryManager
import json
from lo_bot.src.plugins.plugins_manager import PluginsManager
class ChatFlow:
    def __init__(self):
        self.pm=PluginsManager()
        self.ai_chat=LLMClient()
        self.memory_manager=MemoryManager()
        self.memory= self.memory_manager.read_memory()
        self.ai_chat.msg["system"].append({"role":"system","content":f"这是你的记忆:{self.memory}"})
    async def initialize(self) :
         await self.memory_manager.connect()

    async def process_msg(self,msg_info)->str:
        logger.info("处理消息")
        msg=msg_info["msg"]
        logger.info(f"Received message: {msg}")
        _msg=await self.ai_chat.think(msg)
        logger.info("洛洛 思考结果:",_msg)
        try :
            # 尝试解析 JSON
            logger.info("当前prompts:",self.ai_chat.msg["system"])
            t_msg=json.loads(_msg)
            match t_msg:
                case ["plugin",plugin_name]: 
                    logger.info("使用插件")
                    t_reply=await self.use_plugin(plugin_name,msg)
                    logger.info(f"插件结果: {t_reply}")
                    self.ai_chat.msg["system"].append({"role":"system","content":f"{t_reply}是你使用{plugin_name}工具的结果"})
                    logger.info(f"添加插件结果到系统prompt: {self.ai_chat.msg['system'][-1]}")
                    reply=await self.ai_chat.chat(t_reply)
                case _:
                    logger.info("普通消息")
                    reply=await self.ai_chat.chat(msg,user_name=msg_info["nickname"],user_id=msg_info["user_id"])
        except Exception as e:
            logger.error(f"JSON 解析失败: {e}")
            logger.error(f"AI 返回内容: {_msg}")
            # 如果解析失败，直接使用原始消息进行聊天
            reply=await self.ai_chat.chat(msg,user_name=msg_info["nickname"],user_id=msg_info["user_id"])
            logger.info(f"直接聊天结果: {reply}")
        
        await self.add_history(msg_info,reply)
        return reply
    async def add_history(self,msg_info:Dict,rsp_bot:str):
        await self.memory_manager.write_memory(msg_info,rsp_bot)
    async def use_plugin(self,plugin_name,msg=None):
        rsp=await self.pm.to_plugin(plugin_name,msg)
        return rsp





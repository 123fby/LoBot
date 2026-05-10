
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from loguru import logger
from typing import Dict,Any,List
from lo_bot.src.core.llm.llm_client import LLMClient
from lo_bot.src.core.memory.memory_manager import MemoryManager
from lo_bot.src.plugins.plugins_manager import PluginsManager
from lo_bot.src.logic.handle_func.msg_handle import msg_limit,assemble_memory,msg_extract,load_whitelist,msg_filter
class ChatFlow:
    def __init__(self):
        self.pm=PluginsManager()
        self.ai_chat=LLMClient()
        self.memory_manager=MemoryManager()
    async def initialize(self) :
         await self.memory_manager.connect()
         self.memory= await self.memory_manager.init_mem()   
         self.ai_chat.msg["query_memory"].append({"role":"user","content":f"<query>这是你的记忆:{self.memory}</query>"})
         logger.info(f"落落记起来啦！{self.memory}")
         self.whitelist=await load_whitelist()
         logger.info(f"白名单加载完成")
    async def process_msg(self,msg_info)->str:
        logger.info("处理消息") 
        if await msg_filter(msg_info,self.whitelist) == False:
            logger.info("消息不在白名单中，已过滤")
            return 
        msg=msg_info["msg"]
        logger.info(f"Received message: {msg}")
        _msg=await self.ai_chat.chat(msg,user_name=msg_info["nickname"],user_id=msg_info["user_id"])
        logger.info(f"洛洛 思考结果:{_msg}")
        try :
            t_msg=await msg_extract(_msg)#t_msg是一个字典，包含plain_msg,ability和weight
            logger.info(f"提取消息: {t_msg}")
            match t_msg:
                case {"ability": {"plugin": plugin_name}}:
                    logger.info("使用插件")
                    t_reply=await self.use_plugin(plugin_name[0],kwarg=plugin_name[1:])
                    logger.info(f"插件结果: {t_reply}")
                    result=f"<query>{t_reply}是你使用{plugin_name}工具的结果</query>"
                    reply=await self.ai_chat.chat(result,user_name="system",abilitys="plugin")
                case{"ability": {"memory": memory_query}}:
                    logger.info("使用记忆")
                    pass
                case _:
                    logger.info("普通消息")
                    reply=t_msg["plain_msg"]
        except Exception as e:
            logger.error(f"xml解析失败: {e}")
            logger.error(f"AI 返回内容: {_msg}")
            # 如果解析失败，结束本次对话。
            return
        
        await self.add_history(msg_info,str(reply))
        logger.info(f"洛洛 回复: {reply}")
        await msg_limit(self.ai_chat.msg["user"],max_tokens=2048)
        await msg_limit(self.ai_chat.msg["query_memory"],max_tokens=1024)
        return reply
    async def add_history(self,msg_info:Dict,rsp_bot:str):
        await self.memory_manager.write_memory(msg_info,rsp_bot)
    async def use_plugin(self,plugin_name,msg=None,**kwargs):
        rsp=await self.pm.to_plugin(plugin_name,msg,**kwargs)
        return rsp





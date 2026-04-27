
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from lo_bot.src.core.llm.llm_client import LLMClient
from lo_bot.src.core.memory.memory_write import MemoryManager
import json
class ChatFlow:
    def __init__(self,plugins_manager):
        self.pm=plugins_manager
        self.ai_chat=LLMClient()
        self.memory_manager=MemoryManager()
        self.memory= self.memory_manager.read_memory()
        self.ai_chat.msg.append({"role":"system","content":f"这是你的记忆:{self.memory}"})
    async def process_msg(self,msg)->str:
        print("处理消息")
        _msg=await self.ai_chat.think(msg)
        print("洛洛 思考结果:",_msg)
        try :
            # 尝试解析 JSON
            print("当前记忆:",self.ai_chat.msg)
            t_msg=json.loads(_msg)
            match t_msg:
                case ["plugin",plugin_name]: 
                    print("使用插件")
                    t_reply=await self.use_plugin(plugin_name,msg)
                    print(f"插件结果: {t_reply}")
                    self.ai_chat.msg.append({"role":"system","content":f"{t_reply}是你使用{plugin_name}工具的结果"})
                    reply=await self.ai_chat.chat(t_reply)
                case _:
                    print("普通消息")
                    reply=await self.ai_chat.chat(msg)
        except Exception as e:
            print(f"JSON 解析失败: {e}")
            print(f"AI 返回内容: {_msg}")
            # 如果解析失败，直接使用原始消息进行聊天
            reply=await self.ai_chat.chat(msg)
            print(f"直接聊天结果: {reply}")
        
        await self.add_history(msg,reply)
        return reply
    async def add_history(self,rsp_user:str,rsp_bot:str):
        await self.memory_manager.write_memory(rsp_user,rsp_bot)
    async def use_plugin(self,plugin_name,msg=None):
        rsp=await self.pm.to_plugin(plugin_name,msg)
        return rsp





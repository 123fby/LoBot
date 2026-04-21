from pathlib import Path
from datetime import datetime
from lo_bot.src.core.llm.llm_client import LLMClient
import json
import os
from loguru import logger
class MemoryManager:
    def __init__(self):
        self.llm_client = LLMClient()
        self.memory_dir = Path("lo_bot/src/core/memory/memory.json")
        self.time : str=""
    async def write_memory(self,rsp_user:str,rsp_bot:str):
        await self.get_time()
        if os.path.getsize(self.memory_dir)==0:
                data={}
        else:
            with open(Path(self.memory_dir),"r",encoding="utf-8") as f:
                data=json.load(f)      #空文件读取会直接报错   
        data[self.time]={
            "user":rsp_user,
            "bot":rsp_bot,
        }
        if len(data)>8:
            """
            next()拿到第一个键,iter()拿到键的迭代器""" 
            data.pop(next(iter(data)))
            logger.info("删除旧短期记忆")
        with open(Path(self.memory_dir),"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

    async def get_time(self):
        self.time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def read_memory(self)->dict:
        try :
            with open(Path(self.memory_dir),"r",encoding="utf-8") as f:
                data=json.load(f)
                return data
        except FileNotFoundError as e:
            logger.error(e)
            logger.info("创建新记忆啦")
            data={}

from pathlib import Path
from datetime import datetime
from lo_bot.src.core.llm.llm_client import LLMClient
import json
import os
from typing import Dict,Any,List
from loguru import logger
from lo_bot.src.core.memory.PG.conncet import PGConnection
from lo_bot.src.core.memory.PG.short_item import ShortItem

class MemoryManager:
    def __init__(self):
        self.llm_client = LLMClient()
        self.pg_connection=PGConnection()
        self.memory_dir = Path("lo_bot/src/core/memory/memory.json")
        self.short_item=ShortItem(self.pg_connection)
        self.time : str=""
    async def connect(self) :
        await self.pg_connection.connect()
        await self.short_item.create_short_item()

    async def write_memory(self,msg_info:Dict,rsp_bot:str):
        await self.short_item.insert_msg(msg_info,rsp_bot)
    async def init_mem(self):
        return await self.short_item.get_short_item()
       
     
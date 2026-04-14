from pathlib import Path
from datetime import datetime
from lo_bot.src.core.llm.llm_client import LLMClient
import json
class Memorywrite:
    def __init__(self):
        self.llm_client = LLMClient()
        self.memory_dir = Path("lo_bot/src/core/memory/memory.json")
        self.rsp_bpt : str=""
        self.rsp_user : str=""
        self.time
    async def write_memory(self):
        self.rsp_bot=self.llm_client.rsp
        self.rsp_user=self.llm_client.user_history
        await get_time()
        with open(Path(self.memory_dir),"a",encoding="utf-8") as f:
            json.dump(self.time,f,ensure_ascii=False)
            
    async def get_time(self):
        time=datetime.now()
        self.time=time.strftime("%Y-%m-%d %H:%M:%S")

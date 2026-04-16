
from lo_bot.src.core.llm.llm_client import LLMClient
from lo_bot.src.core.memory.memory_write import Memorywrite
class ChatFlow:
    def __init__(self):
        self.ai_chat=LLMClient()
        self.memory_write=Memorywrite()
    async def process_msg(self,msg:str)->str:
        reply=await self.ai_chat.chat(msg)
        await self.add_history(msg,reply)
        return reply
    async def add_history(self,rsp_user:str,rsp_bot:str):
        await self.memory_write.write_memory(rsp_user,rsp_bot)
    





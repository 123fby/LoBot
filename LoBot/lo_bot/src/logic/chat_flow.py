
from lo_bot.src.core.llm.llm_client import LLMClient
class ChatFlow:
    def __init__(self):
        self.ai_chat=LLMClient()
    async def process_msg(self,msg:str)->str:
        reply=await self.ai_chat.chat(msg)
        return reply

    





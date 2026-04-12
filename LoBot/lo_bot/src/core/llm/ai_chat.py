from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class AIChat:
    def __init__(self):
        self.API_KEY:str=os.getenv("API_KEY")
        self.BASE_URL:str=os.getenv("BASE_URL")
        self.client:AsyncOpenAI=AsyncOpenAI(
            api_key=self.API_KEY,
            base_url=self.BASE_URL,
            timeout=60,
        )
        self.msg=[]
        self.rsp:str=""
        self.msg.append({"role":"system","content":"你是龙洛洛,是个阳光开朗的女孩"})   
    async def chat(self,prompt:str) -> str:
        try: 
            self.msg.append({"role":"user","name":"纪念","content":prompt})
            response=await self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2", 
            messages=self.msg,
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
        )
            self.rsp=response.choices[0].message.content.strip() 
            await self.add_history()
            return self.rsp
        except Exception as e:
            return f"AI 调用失败: {str(e)}" 
    async def add_history(self):
        self.msg.append({"role":"assistant","content":self.rsp})
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import toml
from pathlib import Path

load_dotenv()
with open(Path("lo_bot/src/core/memory/character_profile.toml"),"r",encoding="utf-8") as f:
    character_profile=toml.load(f)
class LLMClient:
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
        self.user_history:str=""
        self.msg.append({"role":"system","content":f"你是{character_profile['name']},以下是你的个人信息:{character_profile}"})   
    async def chat(self,user_history:str ) -> str:
        try: 
            self.user_history=user_history
            self.msg.append({"role":"user","name":"纪念","content":self.user_history})
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
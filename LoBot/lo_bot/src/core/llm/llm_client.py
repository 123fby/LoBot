from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import toml
import json
from pathlib import Path
from loguru import logger

load_dotenv()
with open(Path("lo_bot/src/core/memory/character_profile.toml"),"r",encoding="utf-8") as f:
    character_profile=toml.load(f)
with open(Path("lo_bot/src/core/memory/languge_style.toml"),"r",encoding="utf-8") as f:
    language_style=toml.load(f)
with open(Path("lo_bot/src/logic/plugin_map/map.json"),"r",encoding="utf-8") as f:
    plugin_map=json.load(f)

class LLMClient:
    def __init__(self):
        self.API_KEY:str=os.getenv("API_KEY")
        self.BASE_URL:str=os.getenv("BASE_URL")
        self.client:AsyncOpenAI=AsyncOpenAI(
            api_key=self.API_KEY,
            base_url=self.BASE_URL,
            timeout=60,
        )
        self.msg={}
        self.temp_msg=[]
        self.user_history:str=""
        self.prompt=[{"role":"system","content":f"你是{character_profile['name']},以下是你的个人信息:{character_profile},说话风格:{language_style}"}]
        self.msg["system"]=self.prompt
        self.msg["user"]=[]
       
    async def chat(self,user_history:str ,user_name:str=None,user_id:str=None) -> str:
        try: 
            self.user_history=user_history
            self.msg["user"].append({"role":"user","content":f"用户名称:{user_name},用户ID:{user_id},用户对话:{user_history}"})
            msg=self.msg["system"][-3:]+self.msg["user"][-10:]
            response=await self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V4-Flash", 
            messages=msg,
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
        )
            self.rsp=response.choices[0].message.content.strip() 
            await self.manage_history()
            return self.rsp
        except Exception as e:
            return f"AI 调用失败: {str(e)}" 
    async def think(self, user_history: str):
        """思考决策，不参与对话"""
        try: 
            self.user_history = user_history
            # 改进提示词，更明确地要求返回 JSON 格式
            think_prompt = f"""
你是{character_profile['name']}，你需要根据用户的历史对话，思考决策，不参与对话。
以下是插件映射：{plugin_map}

**重要要求：**
1. 如果你决定使用插件，请严格按照以下格式返回：["plugin","插件名称"]
   例如：["plugin","divination"]
   插件名称必须是 {plugin_map.keys()} 中的一个
2. 如果你决定不使用插件，只进行正常聊天，请严格返回：[]
3. 你的回答必须是有效的 JSON 格式，不能包含任何其他文本
4. 不要添加任何解释、对话或其他内容，只返回 JSON 格式

用户历史对话：{user_history}
"""
            
            self.temp_msg = self.msg["system"][-6:]
            self.temp_msg.append({"role": "system", "content": think_prompt})
            self.temp_msg.append({"role": "user", "content": self.user_history})
            response = await self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3", 
                messages=self.temp_msg,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9,
            )
            rsp = response.choices[0].message.content.strip() 
            print(f"Think response: {rsp}")
            return rsp
        except Exception as e:
            print(f"Error in think: {str(e)}")
            # 出错时返回空列表，确保 json.loads 不会失败
            return "[]" 
    async def manage_history(self):
        await self.del_history()
        self.msg["user"].append({"role":"assistant","content":self.rsp})
    async def del_history(self):
        if len(self.msg["user"])>10:
            self.msg["user"]=self.msg["user"][-10:]
            logger.info("删除超过上限的临时记忆")
        if len(self.msg["system"])>5:
            self.msg["system"]=self.msg["system"][-5:]
            logger.info("删除超过上限的系统prompt")

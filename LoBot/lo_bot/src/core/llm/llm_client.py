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
TAG_SCHEMA={
    "reply":{
        "description":"包裹回复内容的标签，必须包含在回复中的最外层标签",
    },
    "text":{
        "description":"文本消息标签，包含要发送的文本内容",
    },
    "emoji":{
        "description":"表情消息标签，包含要发送的表情符号,可选标签，频率不要太高",
    },
    "plugin":{
        "description":"插件调用标签，包含要调用的插件名称和参数",
        "notice":"该标签不会直接返回给用户，而是系统会根据该标签调用相应的插件，并将插件的结果作为系统消息注入到对话中，供你后续对话使用",
        "example":"<plugin>divination,*</plugin>，表示调用占卜插件,*为任意参数，如果需要的话说，可以是任何字符串，插件会根据参数进行处理，警告<lpuhin>标签内只能有一个插件调用",
    },
    "memory":{
        "description":"""记忆标签,包含你想查询的记忆内容,或者描述,通过embedings向量数据库查询相关记忆,并将结果返回给你,
            返回给你时会通过对话注入,例如:<memory>查询关于xx的记忆</memory>,
            系统会将查询结果作为系统消息注入到对话中,例如:{"role":"user","content":"<query>查询记忆的结果:xxx</query>"},然后你就可以根据查询结果进行对话了""",
        "notice":"该标签不会直接返回给用户，而是系统会根据该标签调用相应的插件，并将插件的结果作为系统消息注入到对话中，供你后续对话使用",   
    },
    "weight":{
        "description":"权重标签,这段对话的重要程度,范围是1-10,必要标签,越高记忆遗忘速度越慢,由你自己判断weight的数值",
    },
    "query":{
        "description":"查询标签,这是系统注入的标签,包含memory或者plugin之类查询的结果,你可以根据这个结果进行对话,例如:<query>查询记忆的结果:xxx</query>",
    }
}
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
        self.prompt=[{"role":"system","content":f"""你是{character_profile['name']},以下是你的个人信息:{character_profile},说话风格:{language_style}
                      ,回复时忽略用户ID,用户名称和用户ID仅用于告诉你是谁在与你聊天,回复时请使用xml格式,并且回复内容必须包含在<reply>标签内,
                      例如:<reply>
                              <text>你好！</text>
                              <emoji>😊</emoji>
                                        </reply>
                      硬性规定如下:
                    1. 回复内容必须包含在<reply>标签内
                    2. 标签及描述如下: {TAG_SCHEMA}
                    3.<query>标签是系统注入标签，你不可以使用，其他标签只能在<reply>标签内使用,并且只能使用一次
                    4. 回复必须使用xml格式,不允许添加任何多余的文本,符号或者标签，如:好的,我将使用xml格式回复你!这是错误的回复，因为它包含了多余的文本"好的,我将使用xml格式回复你!"
                    5. <reply>标签外部不允许有任何文本，符号等任何内容
                    6.<reply>标签内的标签不允许进行嵌套，例如:<text>这是<emoji>😊</emoji></text>,错误的回复，因为<text>标签内嵌套了<emoji>标签
                    7.请严格按照上述要求回复,不允许有任何违反规定的回复,如果你无法遵守这些规定,系统将无法·解析你的回复,并且你也无法正常与用户进行对话"
                    """}]
        self.msg["system"]=self.prompt
        self.msg["user"]=[]
        self.msg["query_memory"]=[]
    async def chat(self,user_history:str ,user_name:str=None,user_id:str=None,abilitys=None) -> str:
        try: 
            tool_msg={"tools":[]}
            if user_name=="system" and user_id == None and abilitys==plugin:
                tool_msg["tools"]=[{"role":"system","content":f"<query>{user_history}</query>"}]
            elif user_name=="system" and user_id == None and abilitys==memory:
                self.msg["query_memory"].append({"role":"system","content":f"<query>{user_history}</query>"})
            else :
                self.msg["user"].append({"role":"user","content":f"{user_name}:{user_id}在和你聊天,消息:{user_history}"})
            msg=self.msg["system"]+self.msg["user"]+tool_msg["tools"]+self.msg["query_memory"]
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
#     async def think(self, user_history: str):
#         """思考决策，不参与对话"""
#         try: 
#             self.user_history = user_history
#             # 改进提示词，更明确地要求返回 JSON 格式
#             think_prompt = f"""
# 你是{character_profile['name']}，你需要根据用户的历史对话，思考决策，不参与对话。
# 以下是插件映射：{plugin_map}

# **重要要求：**
# 1. 如果你决定使用插件，请严格按照以下格式返回：["plugin","插件名称"]
#    例如：["plugin","divination"]
#    插件名称必须是 {plugin_map.keys()} 中的一个
# 2. 如果你决定不使用插件，只进行正常聊天，请严格返回：[]
# 3. 你的回答必须是有效的 JSON 格式，不能包含任何其他文本
# 4. 不要添加任何解释、对话或其他内容，只返回 JSON 格式
# 5. 不允许添加其他符号
# 用户历史对话：{user_history}
# """
            
#             self.temp_msg = self.msg["system"][-6:]
#             self.temp_msg.append({"role": "system", "content": think_prompt})
#             self.temp_msg.append({"role": "user", "content": self.user_history})
#             response = await self.client.chat.completions.create(
#                 model="deepseek-ai/DeepSeek-V3", 
#                 messages=self.temp_msg,
#                 temperature=0.7,
#                 max_tokens=1024,
#                 top_p=0.9,
#             )
#             rsp = response.choices[0].message.content.strip() 
#             print(f"Think response: {rsp}")
#             return rsp
#         except Exception as e:
#             print(f"Error in think: {str(e)}")
#             # 出错时返回空列表，确保 json.loads 不会失败
#             return "[]" 
    async def manage_history(self):
        self.msg["user"].append({"role":"assistant","content":self.rsp})


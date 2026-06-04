from openai import AsyncOpenAI, APITimeoutError,RateLimitError,AuthenticationError,BadRequestError
from loguru import logger
class opanai_adapter():
    model_lists=["deepseek-ai/DeepSeek-V4-Flash","deepseek-ai/DeepSeek-V3.2","Pro/deepseek-ai/DeepSeek-V3.2"]
    def __init__(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.count=3
        self.model_pos=0
        self.model=model_lists[self.model_pos]
        self.client: AsyncOpenAI=AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=60
        )
    async def chat(self,model:list[str]=None,
            messages:list[str]=None,temperature:float=0.7,
            max_tokens:int=1024,top_p:float=0.9,**kwargs):  
        msg=messages      
        try:
            model=self.model
            response=await self.client.chat.completions.create(
                model=model,
                messages=msg,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
            return response
        except APITimeoutError as e:
            logger.error(f"请求超时 ฅ{e}")
            await self.retry(msg=msg)
        except RateLimitError as e:
            logger.error(f"请求过于频繁或余额不足 ฅ {e}")
        except AuthenticationError as e:
            logger.error(f"API Key 无效!")
        except BadRequestError as e:
            logger.error (f"参数错误，呜呜呜")
        except Exception as e:
            logger.error(f"诶嘿，洗大锅，我也不知道是什么异常ฅ\n{e}")

    async def retry(self,msg:list[str]=None):
        messages=msg
        if self.count>0:
            logger.warning(f"第{3-self.count+1}次尝试喵")
            self.count-=1
            await self.chat(model=self.model,msg=messages,temperature=0.7,max_tokens=1024,top_p=0.9)
           
        else:
            logger.error(f"重试次数结束，即将切换模型喵！")
            self.swicth_model()
            self.count=3
    def swicth_model(self):
        if self.model_pos>2:
            logger.error(f"模型用尽啦喵，本轮对话强制结束喵")
            self.model_pos=0
            return
        self.model_pos+=1
        logger.info(f"即将切换到{model_lists[self.model_pos]}")
        self.model=model_lists[self.model_pos]








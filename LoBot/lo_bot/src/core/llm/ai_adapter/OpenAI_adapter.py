from openai import AsyncOpenAI, APITimeoutError,RateLimitError,AuthenticationError,BadRequestError
from loguru import logger
from .custom_error import RetryableError
from .shared import Retry
class OpanAI_Adapter():
    model_lists=["deepseek-ai/DeepSeek-V4-Flash","deepseek-ai/DeepSeek-V3.2","Pro/deepseek-ai/DeepSeek-V3.2"]
    def __init__(self,api_key,base_url):
        self.api_key=api_key
        self.base_url=base_url
        self.model=self.model_lists[0]
        self.client: AsyncOpenAI=AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=60
        )

    @Retry(count=3,model_lists=model_lists)
    async def chat(self,model:str=None,
            messages:list[str]=None,temperature:float=0.7,
            max_tokens:int=1024,top_p:float=0.9,timeout:int =10,**kwargs) ->str|bool:
        msg=messages
        model=model or self.model
        self.model=model      
        try:
            response=await self.client.chat.completions.create(
                model=model,
                messages=msg,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                timeout=timeout,
                **kwargs
            )
            return response
        except APITimeoutError as e:
            logger.error(f"请求超时 ฅ{e}")
            raise RetryableError(f"请求超时，重试一次喵\n{e}")
        except RateLimitError as e:
            logger.error(f"请求过于频繁或余额不足 ฅ {e}")
        except AuthenticationError as e:
            logger.error(f"API Key 无效!")
        except BadRequestError as e:
            logger.error (f"参数错误，呜呜呜")
        except Exception as e:
            logger.error(f"诶嘿，洗大锅，我也不知道是什么异常ฅ\n{e}")










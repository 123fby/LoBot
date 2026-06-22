import re
from typing import Any, Dict, List
from .custom_error import RetryableError
from loguru import logger
from types import functools
class Retry:
    def __init__(self,count:int=3,model_lists:List[str]=None):
        self.count=count
        self.model_lists=model_lists
        self.model=self.model_lists[0]
        self.timeout:int=None
        self.index_count=len(self.model_lists)
    def __call__(self,func):
        @functools.wraps(func)#保护原函数信息
        async def wrapper(instance:object,*args,**kwargs):
            """instance:object 被装饰对象，可通过这来修改对象属性"""
            stack=[]
            while self.model_lists.index(self.model)<self.index_count:
                for i in range(self.count):
                    try:
                        kwargs["model"]=self.model
                        result=await func(instance,*args,**kwargs)
                        return result
                    except RetryableError as e:
                        stack.append({
                        "error":e,
                        "count":i,
                    })
                    logger.warning(f"retry {i} \n{e}")
                logger.error(f"retry {self.count} times failed \n{stack}")
                logger.warning(f"重试次数结束，即将切换模型喵！")
                stack.clear()
                new_model=await self.switch_model()
                if new_model!=None:
                    instance.model=new_model
                    
                else:
                    break            
        return wrapper
    async def switch_model(self):
        if self.model_lists.index(self.model)+1 < self.index_count:
            self.model=self.model_lists[self.model_lists.index(self.model)+1]
            logger.warning(f"切换模型为{self.model}")
            return self.model
        else:
            logger.warning(f"切换次数结束，结束对话喵！")
            return None

      
        
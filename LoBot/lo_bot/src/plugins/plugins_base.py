from abc import ABC, abstractmethod
import asyncio

class PluginsBase(ABC):
    @abstractmethod
    def meta(self) ->str:
        """名称，信息，用处之类"""
        pass

    @abstractmethod
    def is_enable(self) ->bool:
        """是否启用"""
        pass
    
    @abstractmethod
    def set_up(self):
        """加载配置之类的"""
        pass
    @abstractmethod
    async def main(self,question: str):
        """主函数,执行插件逻辑"""
        pass
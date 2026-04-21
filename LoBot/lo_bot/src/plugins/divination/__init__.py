
from lo_bot.src.plugins.plugins_base import PluginsBase

from random import choice
import re
from pathlib import Path
import json
"""占卜插件"""
class Divination(PluginsBase):
    def __init__(self):
        self.rsp:str =""
        self._meta={
            "aliases":["divination","算命","占卜","Divination"],
            "description":"占卜插件",
            "enable":"True"
        }
        self.content=self.set_up()
        self.matche:str =""
   
    def meta(self)->str:
        if self._meta:
            return self._meta
  
    def is_enable(self)->bool:
        return self._meta["enable"]=="True"
     
    async def main(self,question):
        if await self.match(question):
            luck_level=choice(self.content["luck_levels"])
            phrases=choice(luck_level["phrases"])
            self.rsp=f"{question} : {luck_level['level']}->{phrases}"
            return self.rsp
        return
 
    def set_up(self):
        """加载配置"""
        with open(Path(__file__).parent.joinpath("content.json"),"r",encoding="utf-8") as f:
            content =json.load(f)
        return content
    async def match(self,question:str)->bool:
        """匹配是否是占卜"""
        if re.search(r"算命|占卜",question):
            return True
        return False
        
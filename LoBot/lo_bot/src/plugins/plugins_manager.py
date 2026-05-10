import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import json
import importlib
from lo_bot.src.plugins.plugins_base import PluginsBase
from nonebot.log import logger

class PluginsManager:
    def __init__(self):
        self.plugins_path=Path(__file__).parent.parent/"plugins"
        self.logic_path=Path(__file__).parent.parent/"logic/plugin_map"
        self.meta={}
        self.plugins_names=[]
        self.enable_plugins:list[str]=[]
        self.plugin_map={}#未使用
        self.plugin={}
        self.data={}
        self.map={}
        self.remap={}
        self.main()
    def open_file(self,path):
        if os.path.getsize(path)==0:
            self.data={}
        else:
            with open(path,"r",encoding="utf-8") as f:
                self.data=json.load(f)
    def save_file(self,path):
        with open(path,"w",encoding="utf-8") as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4)
    def load_plugins(self):
        self.plugins_names =[name.name for name in self.plugins_path.iterdir() if name.is_dir() and name.name != "__pycache__"]
        for plugin_name in self.plugins_names:
            try:
                mod=importlib.import_module(f"lo_bot.src.plugins.{plugin_name}")
                plugin = None  # 初始化 plugin 变量
                plugin_class_name = None  # 初始化类名变量
            
                for name in dir(mod):
                    cls=getattr(mod,name)#获取类
                    if isinstance(cls,type) and issubclass(cls,PluginsBase) and name != "PluginsBase":
                        """依次判断是否是类，是否继承插件基类，排除基类自己"""
                        plugin=cls()                      
                        plugin_class_name = name
                        self.plugin[plugin_class_name]=plugin
                        break
                           
                if plugin and plugin_class_name:  # 只有找到插件时才继续
                    self.push_plugin_meta(plugin_class_name, plugin.meta())
                    self.is_enable(plugin_class_name)
                    logger.info(f"load plugins:{plugin_name} success")
                else:
                    logger.warning(f"no valid plugin class found in {plugin_name}")
            except Exception as e:
                logger.error(e)
                logger.error(f"load plugins:{plugin_name} error")
        self.open_file(self.logic_path/"available_plugins.json")
        self.data=self.enable_plugins
        self.save_file(self.logic_path/"available_plugins.json")
        """构建插件映射表"""
        self.build_plugin_map()
        logger.info(f"洛洛的插件都加载完成啦！")
    def is_enable(self,plugin_name) :
       if self.meta[plugin_name]["enable"]=="True":
           self.enable_plugins.append(plugin_name)
       
    def push_plugin_meta(self,plugin_name,plugin_meta):
        if plugin_name not in self.meta:
            self.meta[plugin_name]=plugin_meta
            self.open_file(self.plugins_path/"plugins_meta.json")
            self.data[plugin_name]=self.meta[plugin_name]
            self.save_file(self.plugins_path/"plugins_meta.json")  
  
    def build_plugin_map(self):
        available={}
        for name in self.enable_plugins:
            available[name]=self.meta[name]
        for name ,plugin_meta in available.items():
            # 保存别名列表
            self.plugin_map[name] = plugin_meta
            # 构建 remap 字典
            for alias in plugin_meta["aliases"]:
                self.remap[alias]=name
        # 保存插件映射表
        self.open_file(self.logic_path/"map.json")
        self.data=self.remap
        self.save_file(self.logic_path/"map.json")
        logger.info(f"构建插件映射表完成!Remap: {self.remap}")
    def main(self):
        self.load_plugins()

    async def to_plugin(self,plugin_name,msg=None,**kwargs):
        name=self.remap[plugin_name]
        return await self.plugin[name].main(msg,**kwargs)
    
if __name__ == "__main__":
    pm=PluginsManager()
    
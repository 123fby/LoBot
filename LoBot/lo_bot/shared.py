import toml
from typing import Any, Dict, List
from loguru import logger

def load_config(config_path, **kwargs):
    """
    加载配置文件
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = toml.load(f)
            logger.info(f"配置文件 {config_path} 加载成功")
            return config
    except FileNotFoundError:
        logger.error(f"配置文件 {config_path} 不存在，正在创建...喵ฅ")
        for key, value in kwargs.items():
            if value is None:
                raise ValueError(f"{key}为None,无法创建配置文件，请提供一个默认{key}的值")
            match value:
                case []:
                    item = input(f"请输入 {key} 的值，多个值请用逗号分隔: ")
                    value = list(item.split(",") if item else [])
                case {}:
                    item = input(f"请输入 {key} 的键值对，多个键值对请用逗号分隔，键和值用冒号分隔，例如 key1:value1,key2:value2: ") 
                    value = dict(item.split(":",1)for item in item.split(",") if item)
                case None:
                    logger.error(f"{key} 的值不能为空，请重新输入")
                    value = input(f"请输入 {key} 的值: ")
                case "":
                    value = input(f"请输入 {key} 的值: ")
            kwargs[key]=value
        with open(config_path, "w", encoding="utf-8") as f:
            toml.dump(kwargs, f)
            logger.info(f"配置文件 {config_path} 创建成功")
        load_config(config_path,**kwargs)
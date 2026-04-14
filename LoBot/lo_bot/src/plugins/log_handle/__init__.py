from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config
from nonebot.log import logger
from nonebot.log import LoguruHandler

__plugin_meta__ = PluginMetadata(
    name="log_handle",
    description="",
    usage="",
    config=Config,
)


config = get_plugin_config(Config)
logger.info("log_handle插件加载成功")

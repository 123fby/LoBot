import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter #控制台适配器
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from global_singletion import set_chat_flow
from lo_bot.src.logic.chat_flow import ChatFlow
load_dotenv(Path(".env"))

nonebot.init()
driver = nonebot.get_driver()
@driver.on_startup
async def startup():
    cf=ChatFlow()
    await cf.initialize()
    set_chat_flow(cf)
    logger.info("chat_flow初始化完成")
driver.register_adapter(OneBotAdapter)
nonebot.load_builtin_plugins("echo")
# nonebot.load_plugins("LoBot/lo_bot/plugins")
if Path("lo_bot/src/adapters/qq_entry.py").exists():
    logger.info("存在----------------------------------------------------------------------------------------------")
    nonebot.load_plugin(Path("lo_bot/src/adapters/qq_entry"))
else:
    logger.error("不存在----------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    nonebot.run()
    

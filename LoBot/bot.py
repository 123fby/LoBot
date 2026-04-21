import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter #控制台适配器
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(".env"))
nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(OneBotAdapter)
nonebot.load_builtin_plugins("echo")
# nonebot.load_plugins("LoBot/lo_bot/plugins")
if Path("lo_bot/src/plugins/qq_entry.py").exists():
    print("存在----------------------------------------------------------------------------------------------")
    nonebot.load_plugin(Path("lo_bot/src/plugins/qq_entry"))
else:
    print("不存在----------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    nonebot.run()
   

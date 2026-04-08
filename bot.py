import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter #控制台适配器
from pathlib import Path
nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)
nonebot.load_builtin_plugins("echo")
# nonebot.load_plugins("LoBot/lo_bot/plugins")
if Path("LoBot/lo_bot/plugins").exists():
    print("存在----------------------------------------------------------------------------------------------")
else:
    print("不存在----------------------------------------------------------------------------------------------")
nonebot.load_plugins(Path("LoBot/lo_bot/plugins"))
if __name__ == "__main__":
    nonebot.run()
   

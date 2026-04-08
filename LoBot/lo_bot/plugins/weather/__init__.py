from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from nonebot import on_command
from nonebot.rule import to_me,Rule
from nonebot.adapters import Message,Event
from nonebot.params import CommandArg,ArgPlainText
from nonebot.matcher import Matcher

from .config import Config


"""插件元数据"""
__plugin_meta__ = PluginMetadata(
    name="weather",
    description="",
    usage="",
    config=Config,
)
"""加载插件配置"""
plugin_config =get_plugin_config(Config)
# config = get_plugin_config(Config)
async def is_enable() ->bool :
    return plugin_config.weather_plugin_enabled
# async def is_blacklisted(event:Event)->bool:
#     return event.get_user_id() not in BLACKLIST
    """rule 的多样性写法并且assert (rule & None) is rule,会忽略None"""
# rule1 = Rule(foo_checker)
# rule2 = Rule(bar_checker)

# rule = rule1 & rule2
# rule = rule1 & bar_checker
# rule = foo_checker & rule2
"""rule = Rule(some_checker)
主动使用响应规则判断事件是否符合条件
result: bool = await rule(bot, event, state)#state 会话状态"""
weather = on_command(
    "天气", 
    rule=  is_enable,
    aliases={"weather","查天气"} ,
    priority=plugin_config.weather_command_priority, 
    block=True,
)


@weather.handle()
async def handle_function( args: Message=CommandArg()):
    #await weather,send("天气是...")
    #提取参数纯文本作为地名，并判断是否有效
    if location:= args.extract_plain_text():
        """:=为海象运算符
        跟以下等价：  location = args.extract_explain_text()
                     if location:"""
        await weather.finish(f"在{location}的天气是{location}")#finish会导致后续程序不会执行，send不会
@weather.got("location", prompt="请输入地名")
async def got_location(location:str =ArgPlainText()):#ArgPlainText()表示参数为纯文本，不会包含其他字符
    await weather.finish(f"今天{location}的天气是...")



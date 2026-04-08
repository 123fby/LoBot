from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from nonebot import on_command
from nonebot.rule import to_me,Rule
from nonebot.adapters import Message,Event
from nonebot.adapters.console import Bot,MessageSegment
from nonebot.params import CommandArg,ArgPlainText
from nonebot.matcher import Matcher

from .config import Config
import inspect#获取对象运行时的信息


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
    rule= to_me() & is_enable,
    aliases={"weather","查天气"} ,
    priority=plugin_config.weather_command_priority, 
    block=True,
)
"""is_enable不能加(),因为is_enable()会立即执行这个异步函数,不会返回True或者False,而是返回协程对象,rule需要传递函数,而不是结果"""

@weather.handle()
async def handle_function( matcher: Matcher,args: Message=CommandArg()):
    #await weather,send("天气是...")
    #提取参数纯文本作为地名，并判断是否有效
    # if location:= args.extract_plain_text():
    #     """:=为海象运算符
    #     跟以下等价：  location = args.extract_explain_text()
    #                  if location:"""
    #     await weather.finish(f"在{location}的天气是...")#finish会导致后续程序不会执行，send不会
    if args.extract_plain_text():
        matcher.set_arg("location",args)
@weather.got("location", prompt=MessageSegment.emoji("question")+"请输入地名")#如果key未被设置,会提示用户输入地名
async def got_location(bot: Bot,location:str =ArgPlainText()):#ArgPlainText()表示参数为纯文本，不会包含其他字符
    if location not in ["北京","上海","广州","深圳"]:
        await weather.reject(f"你查询的城市:{location}不支持，请重新输入")
    await weather.send(
        MessageSegment.markdown(
            inspect.cleandoc(#清理多行字符串的多余缩进，统一格式
                  f"""
                  #{location}
                  
                  -今天
                  
                    ☁️ 多云 20℃~28℃
                    """
            )
        )  
      )
    await bot.bell()#响铃



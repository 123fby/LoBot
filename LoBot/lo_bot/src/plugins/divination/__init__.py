from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg,ArgPlainText
from nonebot.matcher import Matcher
from .config import Config

from random import choice
import re
from pathlib import Path
import json

__plugin_meta__ = PluginMetadata(
    name="divination",
    description="",
    usage="",
    config=Config,
)
"""占卜插件"""

config = get_plugin_config(Config)
divination =on_command(
    "占卜",
    rule=to_me(),
    aliases={"divination","看占卜"},
    block=True,
)
with open(Path(__file__).parent.joinpath("content.json"),"r",encoding="utf-8") as f:
    content =json.load(f)
@divination.handle()
async def divination_handle(matcher:Matcher,args: Message=CommandArg()):
    if args.extract_plain_text():
        args=re.search(r"(占卜)",args)
        matcher.set_arg("question",args.group(1))
@divination.got("question", prompt="请输入占卜问题")
async def divination_got(question: str=ArgPlainText("question")):
    luck_level=choice(content["luck_levels"])
    phrases=choice(luck_level["phrases"])
    result=f"{question} : {luck_level['level']}->{phrases}"
    await divination.send(result)


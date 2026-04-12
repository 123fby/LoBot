from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.console import MessageSegment
from nonebot.params import CommandArg,ArgPlainText
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.rule import to_me

import re

from .config import Config
from ...core.llm.ai_chat import AIChat
__plugin_meta__ = PluginMetadata(
    name="AICaht",
    description="AI 聊天插件",
    usage="",
    config=Config,
)
ai_chat=AIChat()
config = get_plugin_config(Config)
AI_chat=on_command(
    "龙洛洛",
    rule=to_me(),
    aliases={"Lolo","lolo","洛洛"},
    block=True,
)
@AI_chat.handle()
async def handle_msg(matcher: Matcher, args: Message= CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("content",args)

@AI_chat.got("content",prompt="请输入你想对洛洛说的话")
async def handle_content(content: str=ArgPlainText("content")):
    if re.search(r"^quit$",content):
        await AI_chat.finish(await ai_chat.chat("拜拜,洛洛"))
    else:
        await AI_chat.send(await ai_chat.chat(content))
   






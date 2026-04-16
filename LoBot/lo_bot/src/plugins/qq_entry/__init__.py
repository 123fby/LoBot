from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message,Event
from nonebot.rule import to_me
from lo_bot.src.logic.chat_flow import ChatFlow
from nonebot import on_message


ai_chat=ChatFlow()
AI_chat=on_message(
    rule=to_me(),
    block=True,
)
@AI_chat.handle()
async def handle_msg(matcher: Matcher, event:Event):
    msg: Message=event.get_message()
    msg_text: str=msg.extract_plain_text()
    ai_msg=await ai_chat.process_msg(msg_text)
    if msg_text:
        await matcher.send(ai_msg)
    else:
        await matcher.send("hello")
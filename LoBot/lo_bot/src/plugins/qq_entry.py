from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message,Event
from nonebot.rule import to_me
from lo_bot.src.logic.chat_flow import ChatFlow
from nonebot import on_message
from lo_bot.src.plugins.plugins_manager import PluginsManager

AI_chat=on_message(
    rule=to_me(),
    block=True,
)
pm=PluginsManager()
ai_chat=ChatFlow(pm)
@AI_chat.handle()
async def handle_msg(matcher: Matcher, event:Event):
    try:
        print("洛洛要处理消息啦")
        msg: Message=event.get_message()
        msg_text: str=msg.extract_plain_text()
        print(f"Received message: {msg_text}")
        ai_msg=await ai_chat.process_msg(msg_text)
        print(f"AI response: {ai_msg}")
        if ai_msg:
            await matcher.send(ai_msg)
            print(f"Sent response: {ai_msg}")
        else:
            await matcher.send("hello")
            print("Sent hello message")
    except Exception as e:
        print(f"Error in handle_msg: {str(e)}")
        await matcher.send(f"处理消息时出错: {str(e)}")
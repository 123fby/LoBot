from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event
from nonebot.rule import to_me
from nonebot import on_message
from global_singletion import get_chat_flow
from lo_bot.src.adapters.event_parser import msg_parser
from loguru import logger


AI_chat=on_message(
    rule=to_me(),
    block=True,
)
@AI_chat.handle()
async def handle_msg(matcher: Matcher, event:Event):
    ai_chat=get_chat_flow()
    try:
        msg_info=await msg_parser(event)
        logger.info(msg_info)
        logger.info("洛洛要处理消息啦")
        ai_msg=await ai_chat.process_msg(msg_info)
        logger.info(f"AI response: {ai_msg}")
        if ai_msg:
            await matcher.send(ai_msg)
            logger.info(f"Sent response: {ai_msg}")
        else:
            await matcher.send("hello")
            logger.info("Sent hello message")
    except Exception as e:
        logger.error(f"Error in handle_msg: {str(e)}")
        await matcher.send(f"处理消息时出错: {str(e)}")
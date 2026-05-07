import asyncpg
from loguru import logger
from lo_bot.src.core.memory.PG.conncet import PGConnection as pg
from typing import Dict
class ShortItem:
    def __init__(self,pg:pg):
        self.pg=pg
    async def create_short_item(self) :
        async with self.pg.pool.acquire() as conn:
            if  await conn.execute("""create table if not exists short_item (
                 id serial primary key,
                create_at timestamptz default now(),
                scene_type text ,
                group_id text,
                user_id text,
                user_name text,
                user_msg text,
                assistant text
              )"""):
                logger.info("创建短期记忆表")
            else:
                logger.error("短期记忆表已存在")
    async def insert_msg(self,msg_info:Dict,rsp_bot:str) :
        async with self.pg.pool.acquire() as conn:
            try:   
                await conn.execute("""insert into short_item (
                    scene_type,
                    group_id,
                    user_id,
                    user_name,
                    user_msg,
                    assistant)
                    values ($1,$2,$3,$4,$5,$6)""",
                    msg_info["scene_type"],
                    msg_info["group_id"],
                    msg_info["user_id"],
                    msg_info["nickname"],
                    msg_info["msg"],
                    rsp_bot)
                logger.info("插入短期记忆")
            except Exception as e:
                logger.error(f"插入短期记忆失败:{e}")
    async def get_short_item(self,user_id=None):
        """
        获取n轮短期记忆
        """
        async with self.pg.pool.acquire() as conn:
            rows=await conn.fetch("""select user_id,user_name ,user_msg,assistant from short_item
            where user_id=$1 order by create_at desc limit $2 """,
            user_id,10)
            return list(reversed(rows))
    async def delete_short_item(self,user_id):
        """
        删除超出限制的记忆
        """

    async def select_short_item(self,user_id):
        """
        用于向量检索记忆
        """
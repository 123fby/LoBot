
import asyncpg
from loguru import logger
import toml
from lo_bot.shared import load_config
class PGConnection:
    def __init__(self):
        self.pool=None
        self.get_config()
    async def connect(self) :
        try :
            self.pool=await asyncpg.create_pool(
            host=self.host,
            port=self.port,#默认端口5432
            database=self.database,
            user=self.user,
            password=self.password,
            max_size=10,
            min_size=5,
            timeout=60,
            )
            logger.info("数据库连接成功")
            async with self.pool.acquire() as conn:
                version=await conn.fetchval(
                    "select version()"
                )
                logger.info(f"数据库连接成功🚀,数据库版本: {version}")

        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise e
    def get_config(self):
        pg_config= load_config("lo_bot/config/pg_config.toml",host="localhost",port="5432",database="",user="",password="")
        self.host=pg_config.get("host")
        self.port=pg_config.get("port")
        self.database=pg_config.get("database")
        self.user=pg_config.get("user")
        self.password=pg_config.get("password")
        logger.info("数据库连接信息加载完成")

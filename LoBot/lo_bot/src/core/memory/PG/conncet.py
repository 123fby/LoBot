
import asyncpg
from loguru import logger
import toml
from pathlib import Path
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
        try:
            with open(Path("lo_bot/config/pg_connect.toml"), "r",encoding="utf-8") as f:
                pg_config = toml.load(f)
                logger.info("数据库连接信息加载成功")
        except FileNotFoundError:
            logger.error("数据库连接信息文件不存在，已创建默认配置文件,请输入配置信息到config/pg_connect.toml")
            default_config={"host":"localhost","port":5432,"database":"","user":"","password":""}
            with open(Path("lo_bot/config/pg_connect.toml"), "w",encoding="utf-8") as f:
                f.write(toml.dumps(default_config))
                logger.info("默认配置文件已创建")
        self.host=pg_config.get("host")
        self.port=pg_config.get("port")
        self.database=pg_config.get("database")
        self.user=pg_config.get("user")
        self.password=pg_config.get("password")
        logger.info("数据库连接信息加载完成")

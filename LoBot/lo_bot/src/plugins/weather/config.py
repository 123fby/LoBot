from nonebot.utils import V
from pydantic import BaseModel,field_validator

"""key 位置等一些东西，就是一些必要的配置"""
class Config(BaseModel):
    """Plugin Config Here"""
    weather_api_key: str ="sk-123456"
    weather_command_priority: int = 10
    weather_plugin_enabled: bool = True


    @field_validator("weather_command_priority")#校验天气命令优先级是否大于1
    @classmethod
    def check_priority(cls, v:int) -> int:
        if v >=1:
            return v
        raise ValueError("weather command priority must be greater than 1")

    
    

from pydantic import BaseSettings


class Config(BaseSettings):
    plugin_author: str = "Suroy"
    plugin_mail: str = "Suroy@qq.com"
    plugin_name: str = "NLP"
    plugin_bot: str = "12345" # 机器人Q号
    plugin_group_id: dict = {'123456': True} # 通知群号
    plugin_status: bool = True # 插件运行状态
    ITPK_API_KEY: str = '1234' # ITPK
    ITPK_APT_SECRET: str = '567'


    class Config:
        extra = "ignore"
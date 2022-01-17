from pydantic import BaseSettings


class Config(BaseSettings):
    plugin_author: str = "Suroy"
    plugin_mail: str = "Suroy@qq.com"
    plugin_name: str = "studyTeen"
    plugin_bot: str = "1142703165" # 机器人Q号
    plugin_group_id: list[str] = ['257426100'] # 通知群号
    plugin_last_time: int = None # 上次执行时间
    plugin_week_status: bool = False # 本周完成状态
    plugin_status: bool = True # 插件运行状态
    plugin_try_num: int = 0 # 插件接收重新输入标记次数


    class Config:
        extra = "ignore"
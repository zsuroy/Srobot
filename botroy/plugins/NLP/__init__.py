#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: @Suroy
@site: https://suroy.cn/
@email: suroy@qq.com
@time: 2022/2/5 1:00 上午
"""

from aiocqhttp.message import escape
from loguru import logger
from nonebot.rule import to_me
from nonebot import get_driver, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment

from . import itpk_api
from .config import Config

__plugin_name__ = '[I]NLP'
__plugin_usage__ = r"""
[Internal plugin]
Internal plugin for natural language conversation.
Based on ITPK api.
Please DO NOT call the plugin *manually*.
""".strip()

global_config = get_driver().config
init_config = Config(**global_config.dict())


nlp = on_message(rule=to_me(), priority=10)

@nlp.handle()
async def NLP(bot: Bot, event: Event):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = str(event.message)
    if init_config.plugin_status:
        reply = await itpk_api.call_NLP_api(message)
    else:
        logger.warning("Invalid NLP api type. Please config them in config.py to enable NL conversation function.")
        reply = "闲聊对话功能未启用，请使用'/help'查看可用命令"

    # print(message, reply)
    if reply:
        # 如果调用机器人成功，得到了回复，则转义之后发送给用户
        await nlp.send(escape(reply))


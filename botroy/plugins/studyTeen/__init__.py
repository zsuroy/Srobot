#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: @Suroy
@site: https://suroy.cn/
@email: suroy@qq.com
@time: 2022/1/15 1:21 上午
"""
import json
import time
from nonebot import get_driver, get_bot, on_command
from .config import Config
from nonebot import require, logger
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageEvent
from nonebot.adapters import MessageTemplate
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.params import State, Arg, CommandArg, ArgPlainText
import httpx


# 载入配置信息
global_config = get_driver().config
init_config = Config(**global_config.dict())

# 定时任务
scheduler = require("nonebot_plugin_apscheduler").scheduler

@scheduler.scheduled_job("cron", hour="10", minute="*/25", second='5', id="study_teen", kwargs={"config": init_config}, timezone='Asia/Shanghai')
async def study_teen_task(config):
    """
    青年大学习完成提醒
    :description: 10:00开始，1次/25m5s
    :param config: dict, 基本配置项
    :return:
    """
    config = config.dict()
    print('<study_teen_task>', config['plugin_status'])
    if config['plugin_status'] and not config['plugin_week_status']:
        try:
            bot = get_bot(config['plugin_bot']) # 得到bot对象
        except KeyError as e:
            logger.info(config['plugin_name'], 'get_bot Error', sep=" ")
            return
        msg = await get_result()
        for i in config['plugin_group_id']:
            await bot.send_group_msg(group_id=i, message=msg, auto_escape=False)
            # await bot.send_private_msg(user_id=776592058, message=msg, auto_escape=False)
        print("Succ")
        init_config.plugin_last_time = time.time()  # 标记当前时间戳
    else:
        logger.info(f"{config['plugin_name']} 插件已关闭")



async def get_result():
    """
    获取返回消息信息
    :return: str
    """
    data = await getStat()
    if not data: return
    data = json.loads(data)
    # record = {"total": 148, "succ_num": 140, "fail_num": 8, "miss": []} # 打卡完成信息
    record = {"total": data["total"], "succ_num": data["succ_num"], "fail_num": data["fail_num"], "miss": data["miss"]} # 打卡完成信息
    if record['total'] == record['succ_num']: # 全部完成
        init_config.plugin_week_status = True # 标记本周已经完成
        msg_temp = "🎉 本周青年大学习已完成，祝大家生活愉快！"
    else:
        msg_temp = f"⏰ 至今青年大学习完成情况：({record['fail_num']}+{record['succ_num']})/{record['total']}\n🎈 ###未完成同学### 🎈\n{record['miss']}"
    return msg_temp


async def getStat():
    """
    取得api接口数据
    :return:
    """
    async with httpx.AsyncClient(verify=False) as client:
        # r = await client.get('http://127.0.0.1/debug/cloudfiles/manage.php?l=4&c=4&api=stat')
        r = await client.get('https://suroy.cn/addon/filesubmit/manage.php?l=4&c=4&api=stat')
        if r.status_code == 200:
            # print(r.text)
            return r.text


# 人为命令解析
studyTeen = on_command("青年大学习",aliases={'Teen'},priority=5)
@studyTeen.handle()
async def studyTeen_(matcher: Matcher, args: Message = CommandArg())-> None:
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/青年大学习 状态，则args为状态
    if plain_text:
        matcher.set_arg("command", args)  # 如果用户发送了参数则直接赋值


@studyTeen.got("command", prompt="👻 你想查询关于青年大学习的什么功能？")
async def studyTeenCom_(bot:Bot, event: Event, command: Message = Arg(), command_name: str = ArgPlainText("command")) -> None:
    """
    获取命令参数
    :param bot:
    :param event:
    :param command: 消息
    :param command_name: 命令名
    :return:
    """
    # print(f"命令：{command_name}")
    if command_name not in ["状态", "关闭", "启动"]:  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
        init_config.plugin_try_num += 1
        if init_config.plugin_try_num < 3: # 限制重试次数
            await studyTeen.reject(command.template(f"🙄 命令：{command_name} 暂不支持，请重新输入！"))
        else:
            init_config.plugin_try_num = 0 # 重置标记次数
            await studyTeen.finish("🙅‍ 命令错误太多，再见了您勒")

    if event.get_user_id != str(event.self_id):
        if command_name == '状态':
            await studyTeen.finish(await studyTeenStatus_(bot, event))
        elif command_name in ['关闭', '启动']:
            await studyTeen.finish(await studyTeenControl_(command_name))


async def studyTeenStatus_(bot, event):
    """
    当前插件服务运行状态
    :return:
    """
    mess = '青年大学习提醒服务： '+str(init_config.plugin_status)+'\n'+'本周完成状态： '+str(init_config.plugin_week_status) + \
           '\n'+'上次通知：'+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(init_config.plugin_last_time)))
    if SUPERUSER:
        message='🧐 我的主人：\n' + mess
    elif await GROUP_ADMIN(bot, event):
        message='尊贵的管理员：\n'+mess
    elif await GROUP_OWNER(bot, event):
        message='尊贵的群主：\n' + mess
    else:
        message='底层群员没有查看权限！一边凉快呆着吧\n'
    return message


async def studyTeenControl_(command: str):
    """
    控制插件启动与关闭
    :param command: str
    :return: str
    """
    if SUPERUSER:
        msg_head = '🧐 我的主人：'
        if command == '关闭':
            init_config.plugin_status = False
            msg = '关闭成功'
        elif command == '启动':
            init_config.plugin_status == True
            msg = '开启成功'
    else:
        msg_head = '🧐 Oh, 朋友：'
        msg = '无权限'

    return msg_head + '\n' + "健康打卡提醒服务" + msg
import requests
import json
from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment


def get_news():
    url ='https://v1.hitokoto.cn/'
    res = requests.get(url)
    c = json.loads(res.text)
    ans = c['hitokoto']+'---->'+c['from']
    print(ans)
    return ans

async def get_url() -> str:
    """
    :return: 早报图片链接
    """
    url="https://api.iyk0.com/60s"
    res = requests.get(url)
    c = json.loads(res.text)
    return c


explain = on_command("每日一句", priority=5)
@explain.handle()
async def explainsend(bot: Bot, event: Event):
    if int(event.get_user_id()) != event.self_id:
        await bot.send(
            event=event,
            message=get_news()
        )



sixty=on_command("60s",aliases={"早报","六十"},priority=5,block=True)
@sixty.handle()
async def dailyReport_(bot:Bot,event:Event):
    img_url=(await get_url())
    if img_url:
        await sixty.send(message=MessageSegment.image(img_url["imageUrl"]))
    else:
        logger.info('获取时出现错误')
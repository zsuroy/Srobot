import aiohttp, json, random
from typing import Optional
from nonebot import logger, get_driver
from .config import Config

global_config = get_driver().config
init_config = Config(**global_config.dict())


async def call_NLP_api(text: str) -> Optional[str]:

    if not text:
        return None

    # 构造请求数据
    api_key = init_config.ITPK_API_KEY
    api_secret = init_config.ITPK_APT_SECRET
    url = "https://i.mly.app/reply"

    payload = json.dumps({
      "content": text,
      "type": 1,
      "from": init_config.plugin_bot,
      "fromName": "风信子"
    })
    header = {
      'Api-Key': api_key,
      'Api-Secret': api_secret,
      'Content-Type': 'application/json'
    }

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession(headers=header) as sess:
            async with sess.post(url, data=payload) as response:

                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    logger.error(f"对话api调用发生错误")
                    return ("对话api调用发生错误 :(")

                resp_text = await response.json()
                if resp_text["data"]:
                    return random.choice(resp_text["data"])["content"]

    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"An error occupied when calling api: {e}")
        return None
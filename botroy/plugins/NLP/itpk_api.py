import aiohttp, json
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
    url = "http://i.itpk.cn/api.php?question=%s&api_key=%s&api_secret=%s" %(text, api_key, api_secret)

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url) as response:

                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    logger.error(f"对话api调用发生错误")
                    return ("对话api调用发生错误 :(")

                resp_text = await response.text()

                if resp_text:
                    return resp_text

    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"An error occupied when calling api: {e}")
        return None
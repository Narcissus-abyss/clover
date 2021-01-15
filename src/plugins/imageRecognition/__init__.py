import httpx
import io
from nonebot import (
    on_message,
)
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from PIL import Image
from .data_source import predict
from typing import Dict, List

recognition = on_message(priority=5)


@recognition.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg: MessageSegment = event.get_message().pop()
    if msg.type == "image":
        async with httpx.AsyncClient() as client:
            image = await client.get(msg.data['url'])
            im = Image.open(io.BytesIO(image.content))
            pre: List[Dict[str, float]] = predict(im)
            if not pre:
                return
            elif pre[0]["score"] > 0.9:
                await recognition.finish(f" 一定是 {pre[0]['name']} 拉")
                return
            elif pre[0]["score"] > 0.7:
                await recognition.finish(f"我猜是 {pre[0]['name']} ")

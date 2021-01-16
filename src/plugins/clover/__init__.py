from nonebot import (
    on_message,
)
from nonebot.adapters.cqhttp import GroupMessageEvent, Message
from nonebot.adapters import Bot
from .model import (
    predict
)

chat = on_message(priority=5)


@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if str(event.group_id) in ["1098933683", "913211173", "993211173"]:
        msg: Message = event.get_message()
        await chat.finish(predict(str(msg)))

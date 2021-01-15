from nonebot import (
    on_message,
)
from nonebot.adapters.cqhttp import GroupMessageEvent, Message
from nonebot.adapters import Bot
from aredis import StrictRedis

redis_client = StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)


save_chat_data = on_message(priority=5)


@save_chat_data.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = str(event.get_message())
    group_id = str(event.group_id)
    with open(f'/var/www/{group_id}_chat.log', 'w') as file:
        if not await redis_client.exists(group_id):
            await redis_client.set(group_id, True)
            await redis_client.expire(group_id, 60)
            file.write("\n")
        file.write(f"{msg}\n")

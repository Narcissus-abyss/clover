from nonebot import (
    on_message,
)
from nonebot.adapters.cqhttp import GroupMessageEvent, MessageSegment, Message
from nonebot.adapters import Bot
from aredis import StrictRedis

redis_client = StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)


save_chat_data = on_message(priority=5, block=False)


@save_chat_data.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg: Message = event.get_message()
    for item in msg:
        if item.type == 'text':
            group_id = str(event.group_id)
            with open(f'/var/www/chat_data/{group_id}_chat.log', 'a+') as file:
                if not await redis_client.exists(group_id):
                    await redis_client.set(group_id, True)
                    await redis_client.expire(group_id, 60)
                    file.write("\n")
                file.write(f"{item.text}\n")

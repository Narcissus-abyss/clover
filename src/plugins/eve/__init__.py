from .config import Config
from nonebot import (
    on_command,
    on_message,
    logger
)
from nonebot.rule import to_me, startswith
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import MessageEvent
from .data_source import redis_client

add = on_command("add", rule=startswith("add"), priority=5)


@add.handle()
async def _(bot: Bot, event: MessageEvent):
    stripped_arg = event.raw_message.split()[1:]
    logger.debug(f"{stripped_arg}, {len(stripped_arg)}")
    if len(list(stripped_arg)) < 2:
        await add.finish("输入错误")
        return
    elif stripped_arg[-1] == '帅':
        await add.finish('咕咕鸟从来不骗人, 不能说这句')
        return
    else:
        logger.debug(stripped_arg)
        keyword, sentence = stripped_arg[0], ''.join(
            str(i) for i in stripped_arg[1:])
        await redis_client.sadd(keyword, sentence)
        await add.finish(f"你说: {keyword}, 我说: {sentence}")


del_event = on_command("del", rule=to_me(), priority=5)


@del_event.handle()
async def _(bot: Bot, event: MessageEvent):
    stripped_arg = event.raw_message.split()[1:]
    logger.debug(f"{stripped_arg}, {len(stripped_arg)}")
    if len(stripped_arg) < 2:
        await add.finish("输入错误")
        return
    key, word = stripped_arg[0], stripped_arg[-1]
    res = await redis_client.srem(key, word)
    if res == 1:
        await del_event.finish("如果你不想听我就不说了")
    else:
        await del_event.finish("我可不想忘记[CQ:face,id=14]")


list_event = on_command("list", rule=startswith("list"), priority=5)


@list_event.handle()
async def _(bot: Bot, event: MessageEvent):
    stripped_arg = event.raw_message.split()[1:]
    logger.debug(f"{stripped_arg}, {len(stripped_arg)}")
    if stripped_arg and len(stripped_arg) == 1:
        res = await redis_client.smembers(stripped_arg[0])
        await list_event.finish(f"{res}")


group = on_message(block=False)


@group.handle()
async def _(bot: Bot, event: MessageEvent):
    sentence = event.raw_message.strip()
    logger.debug(event.get_message())

    if sentence.split()[0] in ['add', 'list', 'del', 'help', 'info', 'jita',
                               '签到', '兑换', '积分', '抽奖', '柏青哥', '积分池']:
        return
    keywords = await redis_client.keys()
    for index, i in enumerate(keywords):
        sub = sentence.find(i)
        if sub != -1:
            word = await redis_client.srandmember(keywords[index])
            await group.finish(word)
            return

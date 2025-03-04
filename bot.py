#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_builtin_plugins()
nonebot.load_plugin("src.plugins.eve")
nonebot.load_plugin("src.plugins.clover")
nonebot.load_plugin("src.plugins.chat_data")


app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()

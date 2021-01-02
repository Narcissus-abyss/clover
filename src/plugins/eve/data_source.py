import httpx
import asyncio
import xmltodict
import json
import yaml
from aredis import StrictRedis

redis_client = StrictRedis(host='localhost', port=6379, decode_responses=True, db=0)


async def search_user_name(name):
    async with httpx.AsyncClient() as client:
        params = {
            "categories": "character",
            "datasource": "serenity",
            "language": "zh",
            "search": name,
            "strict": True
        }
        result = await client.get(f'https://esi.evepc.163.com/latest/search', params=params)
    if "character" in result.json():
        return result.json()['character'][0]
    return None


def security_status_feedback(security):
    if security > 5:
        return "死刷子"
    if security < -2:
        return '你完了, 我叫统合部部长过来反跳你'
    if security < -5:
        return '3v 优秀战士'


async def get_user_info(name):
    async with httpx.AsyncClient() as client:
        character_id = await search_user_name(name)
        if character_id:
            result = await client.get(
                f'https://esi.evepc.163.com/latest/characters/{character_id}/?datasource=serenity')
            info = result.json()
        else:
            return {'result': '查不到啦'}, None
    print(result.json())
    return yaml.dump({
        'name': info['name'],
        '创建日期': info['birthday'],
        '安等': info['security_status'],
        # '简介': info['description'][:30]
    }, allow_unicode=True), security_status_feedback(info['security_status'])


async def search_name(name):
    async with httpx.AsyncClient() as client:
        result = await client.post('https://www.ceve-market.org/api/searchname', data={"name": name})
    return result.json()


async def get_market(name_list):
    tasks = []

    for i in name_list:
        task = asyncio.create_task((market(i)))
        tasks.append(task)

    result = await asyncio.gather(*tasks)
    return result


async def market(goods):
    async with httpx.AsyncClient() as client:
        jita = await client.get(
            f'https://www.ceve-market.org/api/market/region/10000002/system/30000142/type/{goods["typeid"]}.json')
        # ec = await client.get(f'https://www.ceve-market.org/api/market/region/10000023/system/30001984/type/{typeid}.json')

        jita = jita.json()
        # ec = ec.json()
    return {
        goods['typename']: {
            "收购价": format(jita['buy']['max'], ','),
            # "收购池": format(jita['buy']['max'] * jita['buy']['volume'], ','),
            "出售价": format(jita['sell']['min'], ','),
            # "出售池": format(jita['sell']['min'] * jita['sell']['volume'], ','),
        },
            # "EC-P8R": {
            #     "收购价": format(ec['buy']['max'], ','),
            #     # "收购池": format(ec['buy']['max'] * ec['buy']['volume'], ','),
            #     "出售价": format(ec['sell']['min'], ','),
            #     # "出售池": format(ec['sell']['min'] * ec['sell']['volume'], ','),
            # }
    }


async def quick_look(typeid):
    async with httpx.AsyncClient() as client:
        result = await client.post('https://www.ceve-market.org/api/quicklook',
                                   data={"typeid": typeid, "usesystem": "30000142"})
    return json.dumps(xmltodict.parse(result.text))


async def search_price(name):
    result = await get_market(await search_name(name))
    return yaml.dump(result[:3], allow_unicode=True)


async def status():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get('https://esi.evepc.163.com/latest/status')
            return True
        except Exception as why:
            print(why)
            return False


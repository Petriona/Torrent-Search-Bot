import aiohttp
from requests.utils import requote_uri
from youtubesearchpython import VideosSearch

API_1337x = "https://api.abir-hasan.tk/1337x?query={}&limit={}"
API_YTS = "https://api.abir-hasan.tk/yts?query={}&limit={}"
API_PIRATEBAY = "https://api.abir-hasan.tk/piratebay?query={}&limit={}"

async def YouTubeSearch(query):
    sear = VideosSearch(query)
    result = sear.result()['result']
    return result

async def Search1337x(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_1337x.format(query, 50))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []


async def SearchYTS(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_YTS.format(query, 50))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []


async def SearchPirateBay(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(API_PIRATEBAY.format(query, 50))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []

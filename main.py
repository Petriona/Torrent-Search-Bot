# (c) @AbirHasan2005 & Jigar Varma & Hemanta Pokharel & Akib Hridoy

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQueryResultPhoto

from configs import Config
from tool import SearchYTS, SearchAnime, Search1337x, SearchPirateBay

from youtubesearchpython import *

async def youtube_search(query):
    sear = VideosSearch(query)
    result = sear.result()['result']
    return result

TorrentBot = Client(session_name=Config.SESSION_NAME, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
DEFAULT_SEARCH_MARKUP = [
                    [InlineKeyboardButton("Search YTS", switch_inline_query_current_chat="!yts "),
                     InlineKeyboardButton("Go Inline", switch_inline_query="!yts ")],
                    [InlineKeyboardButton("Search ThePirateBay", switch_inline_query_current_chat="!pb "),
                     InlineKeyboardButton("Go Inline", switch_inline_query="!pb ")],
                    [InlineKeyboardButton("Search 1337x", switch_inline_query_current_chat=""),
                     InlineKeyboardButton("Go Inline", switch_inline_query="")],
                    [InlineKeyboardButton("Search Anime", switch_inline_query_current_chat="!a "),
                     InlineKeyboardButton("GO Inline", switch_inline_query_current_chat="!a ")],
                    [InlineKeyboardButton("Developer: @AbirHasan2005", url="https://t.me/AbirHasan2005")]
                ]


@TorrentBot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    try:
        await message.reply_text(
            text="Hello, I am Torrent Search Bot!\n"
                 "I can search Torrent Magnetic Links from Inline.\n\n"
                 "Made by @AbirHasan2005",
            disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
        )
    except FloodWait as e:
        print(f"[{Config.SESSION_NAME}] - Sleeping for {e.x}s")
        await asyncio.sleep(e.x)
        await start_handler(_, message)


@TorrentBot.on_inline_query()
async def inline_handlers(bot, inline):
    search_ts = inline.query
    answers = []
 
    if search_ts == "":
        answers.append(
            InlineQueryResultPhoto(
                title="Help & Usage", 
                photo_url="https://telegra.ph/file/358af58083cc9bc616221.jpg",
                description="Documentation of Hagadmansa Bot ⚡️",
                caption="Documentation of Hagadmansa Bot ⚡️",
                thumb_url="https://telegra.ph/file/8c4c3ccf01f31538f6df9.jpg",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("PirateBay", switch_inline_query_current_chat="!pb ",
                     InlineKeyboardButton("YTS", switch_inline_query_current_chat="!yts "))]])
            )
        )
    elif search_ts.startswith("!pb"):
        if len(search_ts) == 3:
            answers.append(
            InlineQueryResultPhoto(
                title="PirateBay Search", 
                photo_url="https://telegra.ph/file/727d617ab279538ac270f.png",
                description="Type Something To Search On PirateBay...",
                input_message_content=InputTextMessageContent(
                            message_text=f"**PirateBay Search**\n\n**Usage:** @XnWizBot !pb Your Query",
                        ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("PirateBay", switch_inline_query_current_chat="!pb ")]])
            )
        )
        else:
            query = search_ts.split(" ", 1)[-1]
            torrentList = await SearchPirateBay(query)
            if not torrentList:
                answers.append(
                InlineQueryResultPhoto(
                    title="No Results Found", 
                    photo_url="https://telegra.ph/file/d9c9321593231c8fc72a0.png",
                    description=f"Sorry we couldn't found any result for your query {query}.",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No results found for your query `{query}`.",
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pb ")]])
                )
            )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"🟢: {torrentList[i]['Seeders']}, 🔴: {torrentList[i]['Leechers']}📦: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                                             f"**Name:** `{torrentList[i]['Seeders']}`\n"
                                             f"**Size:** `{torrentList[i]['Size']}`\n"
                                             f"**Seeders:** `{torrentList[i]['Seeders']}`\n"
                                             f"**Leechers:** `{torrentList[i]['Leechers']}`\n"
                                             f"**Uploader:** `{torrentList[i]['Uploader']}`\n"
                                             f"**Uploaded on {torrentList[i]['Date']}**\n\n"
                                             f"**Magnet:**\n`{torrentList[i]['Magnet']}`"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pb ")]])
                        )
                    )
    elif search_ts.startswith("!yts"):
        if len(search_ts) == 4:
            answers.append(
            InlineQueryResultPhoto(
                title="YTS Search", 
                photo_url="https://telegra.ph/file/08243a764a30b934d1da9.png",
                description="Type Something To Search On YTS...",
                input_message_content=InputTextMessageContent(
                            message_text=f"**YTS Search**\n\n**Usage:** @XnWizBot !yts Your Query",
                        ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("YTS", switch_inline_query_current_chat="!pb ")]])
            )
        )
        else:
            query = search_ts.split(" ", 1)[-1]
            torrentList = await SearchYTS(query)
            if not torrentList:
                answers.append(
                InlineQueryResultPhoto(
                    title="No Results Found", 
                    photo_url="https://telegra.ph/file/d9c9321593231c8fc72a0.png",
                    description=f"Sorry we couldn't found any result for your query {query}.",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No results found for your query `{query}`.",
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!yts ")]])
                )
            )
            else:
                for i in range(len(torrentList)):
                    dl_links = "- " + "\n\n- ".join(torrentList[i]['Downloads'])
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Language: {torrentList[i]['Language']}\nLikes: {torrentList[i]['Likes']}, Rating: {torrentList[i]['Rating']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**Genre:** `{torrentList[i]['Genre']}`\n"
                                             f"**Name:** `{torrentList[i]['Name']}`\n"
                                             f"**Language:** `{torrentList[i]['Language']}`\n"
                                             f"**Likes:** `{torrentList[i]['Likes']}`\n"
                                             f"**Rating:** `{torrentList[i]['Rating']}`\n"
                                             f"**Duration:** `{torrentList[i]['Runtime']}`\n"
                                             f"**Released on {torrentList[i]['ReleaseDate']}**\n\n"
                                             f"**Torrent Download Links:**\n{dl_links}\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
    else:
        answers.append(
            InlineQueryResultPhoto(
                title="Help & Usage", 
                photo_url="https://telegra.ph/file/358af58083cc9bc616221.jpg",
                description="Documentation of Hagadmansa Bot ⚡️",
                caption="Documentation of Hagadmansa Bot ⚡️",
                thumb_url="https://telegra.ph/file/8c4c3ccf01f31538f6df9.jpg",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("PirateBay", switch_inline_query_current_chat="!pb ",
                     InlineKeyboardButton("YTS", switch_inline_query_current_chat="!yts "))]])
            )
        )
    
    await inline.answer(
        results=answers,
        cache_time=0
    )
        
    

TorrentBot.run()

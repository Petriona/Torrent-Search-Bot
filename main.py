import os
import requests
from tool import SearchYTS
from tool import SearchPirateBay
from pyrogram import Client, filters
from pyrogram.types import InlineQuery
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineQueryResultPhoto
from pyrogram.types import InputTextMessageContent
from pyrogram.types import InlineQueryResultArticle

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PYPI_API = "https://api.safone.tech/pypi?query={}"
WALLHAVEN_API = "https://wallhaven.cc/api/v1/search?q={}&categories=101&purity=100&apikey=JvjUbQRBuYglCzpBJtKzZpTGvJluVpwe"

bot = Client("XnWizBot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN
            )

@bot.on_message(filters.command("start"))
async def start(bot, message):
    
    await message.reply(
            text="Hello, I'm a simple Inline Bot, these are some websites where i can search. I'm not completed yet, my owner is still devoloping me.",
            reply_markup=InlineKeyboardMarkup(
              [[InlineKeyboardButton("PYPI", switch_inline_query_current_chat="!pypi "),
                InlineKeyboardButton("PirateBay", switch_inline_query_current_chat="!pb ")],[
                InlineKeyboardButton("YTS", switch_inline_query_current_chat="!yts ")]]
            )
        )
    
@bot.on_inline_query()
async def inline_handlers(bot, inline):
    
    answers = []
 
    if inline.query == "":
        answers.append(
            InlineQueryResultPhoto(
                title="Help & Usage", 
                photo_url="https://telegra.ph/file/358af58083cc9bc616221.jpg",
                description="Documentation of Hagadmansa Bot ⚡️",
                caption="Documentation of Hagadmansa Bot ⚡️",
                thumb_url="https://telegra.ph/file/8c4c3ccf01f31538f6df9.jpg",
                reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("PYPI", switch_inline_query_current_chat="!pypi "),
                    InlineKeyboardButton("PirateBay", switch_inline_query_current_chat="!pb ")],[
                    InlineKeyboardButton("YTS", switch_inline_query_current_chat="!yts ")]]
                )
            )
        )
    elif inline.query.startswith("!pb"):
        if len(inline.query) == 3:
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
            query = inline.query.split(" ", 1)[-1]
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
    elif inline.query.startswith("!yts"):
        if len(inline.query) == 4:
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
            query = inline.query.split(" ", 1)[-1]
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
                                             f"**Torrent Download Links:**\n{dl_links}",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
    elif inline.query.startswith("!pypi"):
        if len(inline.query) == 5:
            answers.append(
            InlineQueryResultPhoto(
                title="PYPI Search", 
                photo_url="https://telegra.ph/file/67799789f650d838f9ff4.png",
                description="Type Something To Search On PYPI...",
                input_message_content=InputTextMessageContent(
                            message_text=f"**PYPI Search**\n\n**Usage:** @XnWizBot !pypi Your Query",
                        ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("PYPI", switch_inline_query_current_chat="!pypi ")]])
            )
        )
        else:
            query = inline.query.split(" ", 1)[-1]
            pypi = requests.get(PYPI_API.format(query)).json()
            try:
               if pypi['error']:
                 answers.append(
                 InlineQueryResultPhoto(
                    title="No Results Found", 
                    photo_url="https://telegra.ph/file/d9c9321593231c8fc72a0.png",
                    description=f"Sorry we couldn't found any result for your query {query}.",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No results found for your query `{query}`.",
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pypi ")]])
                )
            )
            except:
                answers.append(
                    InlineQueryResultArticle(
                        title=pypi['title'],
                        description=pypi['description'],
                        input_message_content=InputTextMessageContent(
                            message_text=f"**{pypi['title']} {pypi['version']}**\n\n"
                                         f"**Author:** {pypi['author']}\n"
                                         f"**Email:** {pypi['authorEmail']}\n"
                                         f"**Bug Track Url** {pypi['bugtrackUrl']}\n"
                                         f"**Docs Url:** {pypi['docsUrl']}\n"
                                         f"**License:** {pypi['license']}\n\n"
                                         f"**Description:** {pypi['description']}"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("PYPI link", url=pypi['link']),
                            InlineKeyboardButton("Home Page", url=pypi['homePage'])]]
                        ),
                        thumb_url="https://telegra.ph/file/c1d005226d98a74ad1e16.png"
                    )
                )
    elif inline.query.startswith("!wh"):
        if len(inline.query) == 3:
            answers.append(
            InlineQueryResultPhoto(
                title="Wallhaven Search", 
                photo_url="https://telegra.ph/file/727d617ab279538ac270f.png",
                description="Type Something To Search On Wallhaven...",
                input_message_content=InputTextMessageContent(
                            message_text=f"**Wallhaven Search**\n\n**Usage:** @XnWizBot !wh Your Query",
                        ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Wallhaven", switch_inline_query_current_chat="!wh ")]])
            )
        )
        else:
            query = inline.query.split(" ", 1)[-1]
            wh = requests.get(WALLHAVEN_API.format(query)).json()
            if not wh['data']:
                    answers.append(
                    InlineQueryResultPhoto(
                        title="No Results Found", 
                        photo_url="https://telegra.ph/file/d9c9321593231c8fc72a0.png",
                        description=f"Sorry we couldn't found any result for your query {query}.",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No results found for your query `{query}`.",  
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!wh ")]])
                    )
                )
            else:
                for x in range(len(wh['data']))
                    answers.append(
                        InlineQueryResultPhoto(
                            title=f"Wallpaper #{x}",
                            photo_url=wh['data'][x]['thumbs']['large'],
                            description=f"Views: {wh['data'][x]['views']}, Purity: {wh['data'][x]['purity']}, Category: {wh['data'][x]['category']}, Resolution: {wh['data'][x]['resolution']}",
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Download HD", url=wh['data'][x]['path'])]]
                            )
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
                reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("PYPI", switch_inline_query_current_chat="!pypi "),
                    InlineKeyboardButton("PirateBay", switch_inline_query_current_chat="!pb ")],[
                    InlineKeyboardButton("YTS", switch_inline_query_current_chat="!yts ")]]
                )
            )
        )
    
    await inline.answer(
        results=answers,
        cache_time=0
    )
        
    
bot.run()

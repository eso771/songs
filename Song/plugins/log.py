import os, aiohttp
from pyrogram import filters
from Song import app
from config import OWNER_ID, LOG_FILE_NAME


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def Gamebin(text):
    resp = await post("https://batbin.me/api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = "https://batbin.me/" + resp["message"]
    return link


@app.on_message(filters.command("getlog") & filters.user(OWNER_ID))
async def log(client, message):
    try:
        if os.path.exists(LOG_FILE_NAME):
            log = open(LOG_FILE_NAME)
            lines = log.readlines()
            data = ""
            try:
                NUMB = int(message.text.split(None, 1)[1])
            except:
                NUMB = 100
            for x in lines[-NUMB:]:
                data += x
            link = await Gamebin(data)
            return await message.reply_text(link)
    except Exception as e:
        print(f"{e}")

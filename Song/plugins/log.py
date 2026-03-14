from pyrogram import Client, filters
from Song import app

# Log göndəriləcək qrup və ya kanal ID
LOG_CHAT = -1003767974813


# START LOG
@app.on_message(filters.command("start"))
async def start_log(client, message):

    user = message.from_user.mention

    text = f"{user} Bota start etdi ✅"

    await client.send_message(LOG_CHAT, text)


# SONG LOG
@app.on_message(filters.command("song"))
async def song_log(client, message):

    user = message.from_user.mention
    query = message.text.split(None, 1)

    if len(query) > 1:
        song = query[1]
    else:
        song = "Mahnı adı yazılmayıb"

    text = f"{user} {song} yükləməyə çalışır 🎵"

    await client.send_message(LOG_CHAT, text)


# SEARCH LOG
@app.on_message(filters.command("search"))
async def search_log(client, message):

    user = message.from_user.mention
    query = message.text.split(None, 1)

    if len(query) > 1:
        song = query[1]
    else:
        song = "Mahnı adı yazılmayıb"

    text = f"{user} {song} axtarmağa çalışır 🎵"

    await client.send_message(LOG_CHAT, text)

import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from Song import app

search_cache = {}

# ⚡ FAST YOUTUBE SEARCH
def yt_search(query):

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,   # sürətli axtarış
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "geo_bypass": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch30:{query}", download=False)
        return results["entries"]


@app.on_message(filters.command("search"))
async def search_music(client, message):

    if len(message.command) < 2:
        return await message.reply(
            "👀 <b>Axtarış etmək üçün musiqi adı təyin etməlisiniz!</b>"
        )

    query = " ".join(message.command[1:])

    msg = await message.reply("🔍 <b>Məlumatlar əldə edilir...</b>")

    results = yt_search(query)

    if not results:
        return await msg.edit("❌ <b>Nəticə tapılmadı</b>")

    item = results[0]

    video_id = item["id"]
    thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    title = item["title"]
    url = f"https://youtube.com/watch?v={video_id}"
    channel = item.get("uploader", "Naməlum")
    views = item.get("view_count", 0)

    text = f"""
<b>Axtarış nəticəsi:</b> 1/30

🎵 **Başlıq:** <a href="{url}">{title}</a>
📢 **Kanal:** {channel}
👁️ **Baxış:** {views}
🫯 **Platform:** `YouTube`
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️ Geri", callback_data="back"),
            InlineKeyboardButton("➡️ İrəli", callback_data="next")
        ]
        [
            InlineKeyboardButton("❌ Bağla", callback_data="song_close")
        ]
    ])

    await msg.delete()

    sent = await message.reply_photo(
        photo=thumbnail,
        caption=text,
        reply_markup=buttons
    )

    search_cache[sent.id] = {
        "results": results,
        "index": 0
    }


@app.on_callback_query(filters.regex("^(next|back)$"))
async def change_result(client, query):

    msg_id = query.message.id

    data = search_cache.get(msg_id)

    if not data:
        return await query.answer("❌ <b>Nəticə tapılmadı</b>", show_alert=True)

    index = data["index"]
    results = data["results"]

    if query.data == "next":
        if index < len(results) - 1:
            index += 1
    else:
        if index > 0:
            index -= 1

    data["index"] = index

    item = results[index]

    video_id = item["id"]
    thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    title = item["title"]
    url = f"https://youtube.com/watch?v={video_id}"
    channel = item.get("uploader", "Naməlum")
    views = item.get("view_count", 0)

    text = f"""
<b>Axtarış nəticəsi:</b> {index+1}/30

🎵 **Başlıq:** <a href="{url}">{title}</a>
📢 **Kanal:** {channel}
👁️ **Baxış:** {views}
🫯 **Platform:** `YouTube`
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️ Geri", callback_data="back"),
            InlineKeyboardButton("➡️ İrəli", callback_data="next")
        ]
        [
            InlineKeyboardButton("❌ Bağla", callback_data="song_close")
        ]
    ])

    media = InputMediaPhoto(
        media=thumbnail,
        caption=text
    )

    await query.message.edit_media(
        media=media,
        reply_markup=buttons
    )

    await query.answer()


@app.on_callback_query(filters.regex("song_close") & ~BANNED_USERS)
async def close_song(client, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
    except:
        pass
    await CallbackQuery.answer("Menyu Bağlandı ❌")

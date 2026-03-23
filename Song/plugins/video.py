import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
from Song.plugins.YouTube import YouTubeAPI
from Song import app
import yt_dlp

YouTube = YouTubeAPI()

search_cache = {}

# 🔎 YouTube search
async def search_youtube(query: str, limit: int = 30):
    ydl_opts = {"quiet": True, "skip_download": True, "extract_flat": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
        results = []
        for entry in info.get("entries", []):
            results.append({
                "title": entry.get("title"),
                "id": entry.get("id"),
                "duration": entry.get("duration") or 0,
                "thumbnail": entry.get("thumbnail"),
                "views": entry.get("view_count") or 0
            })
        return results

# 🔥 Instagram download
def download_instagram(url):
    ydl_opts = {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path, info

# 🔹 Command
@app.on_message(filters.command("video") & filters.private)
async def video_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Link və ya video adı yaz.")

    query = message.text.split(None, 1)[1].strip()

    # 🔥 Instagram
    if "instagram.com" in query:
        msg = await message.reply_text("📥 Instagram video yüklənir...")

        try:
            file_path, info = download_instagram(query)
        except Exception as e:
            return await msg.edit_text(f"❌ Xəta: {e}")

        caption = f"📸 <b>{info.get('title','Instagram Video')}</b>"

        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=caption
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        return await msg.delete()

    # 🔥 YouTube link
    if "youtu" in query:
        msg = await message.reply_text("🎬 Video yüklənir...")

        try:
            file_path, status = await YouTube.download(query, msg, video=True)
        except Exception as e:
            return await msg.edit_text(f"❌ Xəta: {e}")

        if not status or not file_path:
            return await msg.edit_text("❌ Yükləmə alınmadı")

        title, duration_min, duration_sec, _, _ = await YouTube.details(query)

        caption = (
            f"🎬 <b>Başlıq:</b> <a href='{query}'>{title}</a>\n"
            f"⏰ {duration_min:02}:{duration_sec:02}"
        )

        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=caption,
            duration=int(duration_sec)
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        return await msg.delete()

    # 🔎 YouTube search
    msg = await message.reply_text("🔎 Axtarılır...")

    try:
        results = await search_youtube(query)
    except Exception as e:
        return await msg.edit_text(f"❌ Xəta: {e}")

    if not results:
        return await msg.edit_text("❌ Tapılmadı")

    search_cache[message.from_user.id] = {"results": results, "index": 0}
    await send_result(msg, message.from_user.id)

# 🔹 Result
async def send_result(message_obj, user_id):
    data = search_cache.get(user_id)
    if not data:
        return

    index = data["index"]
    results = data["results"]
    result = results[index]

    yt_url = f"https://www.youtube.com/watch?v={result['id']}"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️", callback_data="prevs"),
            InlineKeyboardButton("🎬 Yüklə", callback_data=f"download {result['id']}"),
            InlineKeyboardButton("➡️", callback_data="nexts"),
        ],
        [
            InlineKeyboardButton("❌ Bağla", callback_data="close")
        ]
    ])

    caption = (
        f"🎬 <a href='{yt_url}'>{result['title']}</a>"
    )

    try:
        await message_obj.delete()
        await message_obj.chat.send_photo(
            photo=result["thumbnail"],
            caption=caption,
            reply_markup=buttons
        )
    except:
        await message_obj.edit_text(caption, reply_markup=buttons)

# 🔹 Next
@app.on_callback_query(filters.regex("nexts"))
async def next_(client, cb):
    data = search_cache.get(cb.from_user.id)
    if data and data["index"] < len(data["results"]) - 1:
        data["index"] += 1
    await send_result(cb.message, cb.from_user.id)
    await cb.answer()

# 🔹 Prev
@app.on_callback_query(filters.regex("prevs"))
async def prev_(client, cb):
    data = search_cache.get(cb.from_user.id)
    if data and data["index"] > 0:
        data["index"] -= 1
    await send_result(cb.message, cb.from_user.id)
    await cb.answer()

# 🔹 Download
@app.on_callback_query(filters.regex("download"))
async def download_video(client, cb):
    vidid = cb.data.split()[1]
    url = f"https://www.youtube.com/watch?v={vidid}"

    await cb.message.edit_caption("🎬 Video yüklənir...")

    file_path, status = await YouTube.download(url, cb.message, video=True)

    title, duration_min, duration_sec, _, _ = await YouTube.details(url)

    await client.send_video(
        chat_id=cb.message.chat.id,
        video=file_path,
        caption=f"🎬 {title}"
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    await cb.message.delete()
    await cb.answer("Yükləndi")

# 🔹 Close
@app.on_callback_query(filters.regex("close"))
async def close_(client, cb):
    await cb.message.delete()
    await cb.answer("Bağlandı")

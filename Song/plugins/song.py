import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
from canfig import BANNED_USERS
from Song.plugins.YouTube import YouTubeAPI
from Song import app
from Song.utils.decorators.language import language, languageCB
import yt_dlp
YouTube = YouTubeAPI()

# 🔹 User cache
search_cache = {}

# 🔎 YouTube search funksiyası
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

# 🔹 /song command (ad və ya link)
@app.on_message(filters.command("song") & filters.private & ~BANNED_USERS)
@language
async def song_search(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text("❌ Mahnı adı yaz.")

    query = message.text.split(None, 1)[1].strip()

    # Əgər YouTube linkidirsə, birbaşa yüklə
    if "youtu" in query:
        mystic = await message.reply_text("🎧 <b>Musiqi yüklənir...</b>")
        try:
            file_path, status = await YouTube.download(
                query,
                mystic,
                songaudio=True
            )
        except Exception as e:
            return await mystic.edit_text(f"❌ Xəta: {e}")

        if not status or not file_path:
            return await mystic.edit_text("❌ Yükləmə xətası")

        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)

        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        new_file_path = f"downloads/{title}.mp3"
        os.rename(file_path, new_file_path)
        file_path = new_file_path

        user_caption = (
            f"🎧 <b>Başlıq:</b> <a href='{query}'>{title}</a>\n"
            f"⏰ <b>Müddət:</b> {duration_min:02}\n\n"
            f"🤖 <b>Bot:</b> @UzeyirMusic_bot"
        )
        user_buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎵 Playlist", url="https://t.me/UzeyirPlaylist")]]
        )
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_path,
            caption=user_caption,
            title=title,
            performer="UzeyirMusic🇦🇿",
            duration=int(duration_sec),
            reply_markup=user_buttons
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        return await mystic.delete()

    # Əks halda əvvəlki axtarış sistemi ilə davam et
    mystic = await message.reply_text("🔎 <b>Axtarılır...</b>")
    try:
        results = await search_youtube(query, limit=30)
    except Exception as e:
        return await mystic.edit_text(f"❌ Xəta baş verdi\n\n{e}")

    if not results:
        return await mystic.edit_text("❌ Nəticə tapılmadı.")

    search_cache[message.from_user.id] = {"results": results, "index": 0}
    await send_result(mystic, message.from_user.id)

# 🔹 send_result funksiyası
async def send_result(message_obj, user_id):
    data = search_cache.get(user_id)
    if not data:
        return

    index = data["index"]
    results = data["results"]
    result = results[index]

    minutes = result["duration"] // 60
    seconds = result["duration"] % 60
    views = result.get("views", 0)
    total = len(results)

    buttons = [
        [
            InlineKeyboardButton("⬅️ Geri", callback_data="song_prev"),
            InlineKeyboardButton("🎧 İndir", callback_data=f"song_download {result['id']}"),
            InlineKeyboardButton("➡️ İrəli", callback_data="song_next"),
        ],
         [
        InlineKeyboardButton("❌ Bağla", callback_data="song_close")
         ]
    ]

    caption = (
        f"🔍 <b>Axtarış nəticəsi:</b> {index + 1}/{total}\n\n"
        f"🎶 <b>Başlıq:</b> <a href='https://www.youtube.com/watch?v={result['id']}'>{result['title']}</a>\n"
        f"⏱️ <b>Müddət:</b> {minutes:02}\n"
        f"👁️ <b>Baxış sayı:</b> <code>{views:,}</code>"
    )

    try:
        if result.get("thumbnail"):
            if isinstance(message_obj, Message):
                await message_obj.delete()
                await message_obj.chat.send_photo(
                    photo=result["thumbnail"],
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            else:
                await message_obj.edit_media(
                    InputMediaPhoto(
                        media=result["thumbnail"],
                        caption=caption
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
        else:
            await message_obj.edit_text(caption, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception:
        await message_obj.edit_text(caption, reply_markup=InlineKeyboardMarkup(buttons))

# 🔹 pagination callbacks
@app.on_callback_query(filters.regex("song_next") & ~BANNED_USERS)
async def next_song(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    data = search_cache.get(user_id)
    if not data:
        return

    if data["index"] < len(data["results"]) - 1:
        data["index"] += 1

    await send_result(CallbackQuery.message, user_id)
    await CallbackQuery.answer()

@app.on_callback_query(filters.regex("song_prev") & ~BANNED_USERS)
async def prev_song(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    data = search_cache.get(user_id)
    if not data:
        return

    if data["index"] > 0:
        data["index"] -= 1

    await send_result(CallbackQuery.message, user_id)
    await CallbackQuery.answer()

# 🔹 download callback
@app.on_callback_query(filters.regex("song_download") & ~BANNED_USERS)
@languageCB
async def download_song(client, CallbackQuery, _):
    vidid = CallbackQuery.data.split()[1]
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    user = CallbackQuery.from_user
    username = f"@{user.username}" if user.username else user.first_name

    await CallbackQuery.message.edit_caption("🎧 <b>Musiqi yüklənir...</b>")

    try:
        file_path, status = await YouTube.download(
            yturl,
            CallbackQuery.message,
            songaudio=True
        )
    except Exception as e:
        return await CallbackQuery.message.edit_caption(f"❌ Xəta: {e}")

    if not status or not file_path:
        return await CallbackQuery.message.edit_caption("❌ Yükləmə xətası")

    title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(yturl)

    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    new_file_path = f"downloads/{title}.mp3"
    os.rename(file_path, new_file_path)
    file_path = new_file_path

    user_caption = (
        f"🎧 <b>Başlıq:</b> <a href='{yturl}'>{title}</a>\n"
        f"⏰ <b>Müddət:</b> {duration_min:02}\n\n"
        f"🤖 <b>Bot:</b> @UzeyirMusic_bot"
    )
    user_buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎵 Playlist", url="https://t.me/UzeyirPlaylist")]]
    )
    await client.send_audio(
        chat_id=CallbackQuery.message.chat.id,
        audio=file_path,
        caption=user_caption,
        title=title,
        performer="UzeyirMusic🇦🇿",
        duration=int(duration_sec),
        reply_markup=user_buttons
    )

    playlist_caption = (
        f"🎧 <b>Başlıq:</b> <a href='{yturl}'>{title}</a>\n"
        f"⏰ <b>Müddət:</b> {duration_min:02}\n"
        f"👤 <b>İstəyən:</b> {username}\n\n"
        f"🤖 <b>Bot:</b> @UzeyirMusic_bot"
    )
    playlist_buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✚ Məni Qrupa Əlavə Et ✚", url="https://t.me/UzeyirMusic_Bot?startgroup=true")]]
    )
    await client.send_audio(
        chat_id="@UzeyirPlaylist",
        audio=file_path,
        caption=playlist_caption,
        title=title,
        performer="UzeyirMusic🇦🇿",
        duration=int(duration_sec),
        reply_markup=playlist_buttons
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    try:
        await CallbackQuery.message.delete()
    except:
        pass

    await CallbackQuery.answer("🎵 Yükləndi!")

# 🔹 Close button
@app.on_callback_query(filters.regex("song_close") & ~BANNED_USERS)
async def close_song(client, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
    except:
        pass
    await CallbackQuery.answer("Menyu Bağlandı ❌")

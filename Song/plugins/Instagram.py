import re
import asyncio
import yt_dlp
from pyrogram import Client, filters
from Song import app

INSTAGRAM_REGEX = r"(https?://(?:www\.)?instagram\.com/[^\s]+)"

def get_type(url):
    if "/reel/" in url:
        return "Reels"
    elif "/p/" in url:
        return "Post"
    elif "/stories/" in url:
        return "Story"
    else:
        return "Media"

@app.on_message(filters.text)
async def insta_downloader(client, message):
    text = message.text

    match = re.search(INSTAGRAM_REGEX, text)
    if not match:
        return

    url = match.group(0)

    msg = await message.reply("🔍 **Link emal edilir**")

    media_type = get_type(url)

    await msg.edit(
        f"🧸 **Link axtarışı tamamlandı**\n"
        f"🌐 **Növ:** {media_type}"
    )

    await asyncio.sleep(3)
    await msg.edit("📥 **Yüklənilir...**")

    ydl_opts = {
        "outtmpl": "insta_%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,

        # 🔥 ƏN VACİB HİSSƏ
        "cookiefile": "cookies.txt",

        # 🔥 BAN yeməmək üçün
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },

        "sleep_interval": 2,
        "max_sleep_interval": 5
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        # 📤 Göndərmə (növə görə)
        if media_type == "Story":
            await message.reply_video(file)
        else:
            await message.reply_video(file)

        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Xəta:\n{str(e)}")

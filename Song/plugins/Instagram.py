import re
import asyncio
import yt_dlp
from pyrogram import Client, filters
from Song import app

# Instagram link regex
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
        return  # başqa linkdirsə heçnə etmə

    url = match.group(0)

    # 🔍 mesaj
    msg = await message.reply("🔍 **Link emal edilir**")

    media_type = get_type(url)

    # edit 1
    await msg.edit(
        f"🧸 **Link axtarışı tamamlandı**\n"
        f"🌐 **Növ:** {media_type}"
    )

    await asyncio.sleep(3)

    # edit 2
    await msg.edit("📥 **Yüklənilir**")

    ydl_opts = {
        "outtmpl": "insta.%(ext)s",
        "quiet": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        # göndər
        await message.reply_video(file)

        # sil
        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Xəta:\n{e}")

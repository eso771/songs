import requests
from pyrogram import filters

from Song import app


@app.on_message(filters.text & ~filters.command)
async def download_instagram_video(client, message):
    text = message.text

    # Yalnız Instagram linki yoxla
    if "instagram.com" not in text:
        return  # başqa linkdirsə heç nə etmə

    a = await message.reply_text("İşleniyor...")

    url = text.strip()
    api_url = f"https://nodejs-1xn1lcfy3-jobians.vercel.app/v2/downloader/instagram?url={url}"

    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()

        if data.get("status") and data.get("data"):
            video_url = data["data"][0]["url"]
            await a.delete()
            await client.send_video(message.chat.id, video_url)
        else:
            await a.edit("❌ Video tapılmadı və ya link düzgün deyil")

    except Exception as e:
        await a.edit(f"❌ Xəta baş verdi:\n{str(e)}")

import os
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Song import app

# ================= SETTINGS =================
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

INSTAGRAM_REGEX = r"(https?://(www\.)?instagram\.com/[^\s]+)"

# ================= PROGRESS BAR =================
def progress_bar(percent: float, total: int = 10):
    filled = int(percent / 100 * total)
    empty = total - filled
    return "█" * filled + "░" * empty

# ================= HANDLER =================
@app.on_message(
    filters.regex(INSTAGRAM_REGEX)
    & (filters.private | filters.group)
)
async def instagram_handler(client, message: Message):
    link = message.text

    status_msg = await message.reply_text(
        "🙋🏻‍♀️ <b>Zəhmət olmasa gözləyin</b>\n"
        "💁🏻‍♀️ <b>Yüklənmə növü:</b> Instagram Reels\n\n"
        "📥 <b>Yüklənir:</b> <code>0%</code>\n"
        "<code>░░░░░░░░░░</code>"
    )

    file_path = os.path.join(DOWNLOAD_DIR, f"instagram_{message.id}.mp4")

    cmd = [
        "yt-dlp",
        "-f", "mp4",
        "--newline",
        "-o", file_path,
        link
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        last_percent = -1
        private_video = False

        while True:
            line = await process.stdout.readline()
            if not line:
                break

            line = line.decode("utf-8", errors="ignore").lower()

            # ===== PRIVATE / FORBIDDEN CHECK =====
            if any(x in line for x in [
                "private",
                "forbidden",
                "403",
                "login required",
                "this video is private"
            ]):
                private_video = True
                break

            # ===== PROGRESS =====
            if "[download]" in line and "%" in line:
                try:
                    percent = float(line.split("%")[0].split()[-1])
                    rounded = int(percent)

                    if rounded != last_percent:
                        last_percent = rounded
                        bar = progress_bar(percent)

                        await status_msg.edit(
                            "🙋🏻‍♀️ <b>Zəhmət olmasa gözləyin</b>\n"
                            "💁🏻‍♀️ <b>Yüklənmə növü:</b> Instagram Reels\n\n"
                            f"📥 <b>Yüklənir:</b> <code>{percent:.1f}%</code>\n"
                            f"<code>{bar}</code>"
                        )
                except:
                    pass

        await process.wait()

        # ===== PRIVATE VIDEO MESSAGE =====
        if private_video:
            await status_msg.edit(
                "🙋🏻‍♀️ <b>Göndərdiyiniz video linki Instagram private hesabında olduğundan yükləyə bilmirəm</b>\n"
                "💁🏻‍♀️ <b>Əgər bunun xəta olduğunu irad edirsinizsə, bizimlə əlaqə saxlayın</b>"
            )
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        # ===== FILE CHECK =====
        if not os.path.exists(file_path):
            await status_msg.edit(
                "🙋🏻‍♀️ <b>Video yüklənmədi</b>\n"
                "💁🏻‍♀️ <b>Əgər bunun xəta olduğunu irad edirsinizsə, bizimlə [əlaqə](https://t.me/Uzeyirrrrrrrrrr) saxlayın</b>"
            )
            return

        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=(
                "🙋🏻‍♀️ <b>Video hazırdır</b>\n"
                "💁🏻‍♀️ <b>Platforma növ:</b> <code>Instagram Reels</code>"
            )
        )

        await status_msg.delete()
        os.remove(file_path)

    except Exception as e:
        await status_msg.edit(f"❌ Xəta baş verdi:\n`{e}`")

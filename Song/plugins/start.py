from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Song import app

OWNER = "Uzeyirrrrrrrrrr"
PLAYLIST = "https://t.me/UzeyirPlaylist"


# START MESAJI
@app.on_message(filters.command("start"))
async def start(client, message):

    user = message.from_user.mention

    text = f"""
**Salam** {user} 👋🏻
**Mən musiqi yükləmək üçün yaradılmış botam** 🤖
**Mənim əmrlərim əmrlər buttonuna klikləyin** 📚
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Məni qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")
            ],
            [
                InlineKeyboardButton("👨🏻‍💻 Sahibim", url=f"https://t.me/{OWNER}"),
                InlineKeyboardButton("🎧 Playlist", url=PLAYLIST)
            ],
            [
                InlineKeyboardButton("📚 Əmrlər", callback_data="commands")
            ]
        ]
    )

    await message.reply_text(text, reply_markup=buttons)


# ƏMRLƏR BUTTON
@app.on_callback_query(filters.regex("commands"))
async def commands(client, query: CallbackQuery):

    text = """
**Music Yükləmək**🇦🇿 üçün komandalar:

🔮 **Komanda:** /song
📜 **Nümunə:** `/song Üzeyir Qara gözlər`
📚 **Açıqlama:** Yazdığınız musiqini yükləyər

🔮 **Komanda:** /search
📜 **Nümunə:** `/search Üzeyir Qara gözlər`
📚 **Açıqlama:** Yazdığınız musiqi haqqında sizə məlumat verər

📢 **Əlavə olaraq, TikTok, Instagram linkləri göndərərək video yükləyə bilərsiniz..**
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅️ Geri", callback_data="back")
            ]
        ]
    )

    await query.message.edit_text(text, reply_markup=buttons)


# GERİ BUTTON
@app.on_callback_query(filters.regex("back"))
async def back(client, query: CallbackQuery):

    user = query.from_user.mention

    text = f"""
**Salam** {user} 👋🏻
**Mən musiqi yükləmək üçün yaradılmış botam** 🤖
**Mənim əmrlərim əmrlər buttonuna klikləyin** 📚
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Məni qrupa əlavə et", url="https://t.me/UzeyirMusic_Bot?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")
            ],
            [
                InlineKeyboardButton("👨🏻‍💻 Sahibim", url=f"https://t.me/{OWNER}"),
                InlineKeyboardButton("🎧 Playlist", url=PLAYLIST)
            ],
            [
                InlineKeyboardButton("📚 Əmrlər", callback_data="commands")
            ]
        ]
    )

    await query.message.edit_text(text, reply_markup=buttons)

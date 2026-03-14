from pyrogram import filters
from youtube_search import YoutubeSearch
from Song import app


@app.on_message(filters.command("search"))
@app.on_edited_message(filters.command("search"))
async def search(client, message):
    if len(message.command) < 2:
        return await message.reply_text("💡İstifadə:\n\n🔗/search (musiqi adı)")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("`🔍Musiqi axtarılır...`")
    results = YoutubeSearch(query, max_results=5).to_dict()
    i = 0
    text = ""
    while i < 5:
        text += f"🖇️Adı -> {results[i]['title']}\n"
        text += f"⏳Müddəti -> {results[i]['duration']}\n"
        text += f"📢Kanal -> {results[i]['channel']}\n"
        text += f"🔗Link -> https://youtu.be/{results[i]['id']}\n\n"
        i += 1
    await m.edit(text, disable_web_page_preview=True)

from pyrogram import filters
from Song import app, loop
from Song.helpers.song import get_url, get_yt_info_query, is_tiktok_url, is_instagram_url, download_social_video
from Song.helpers.inline import song_markup


@app.on_message(filters.text & filters.private & ~filters.command("song") & ~filters.forwarded)
@app.on_edited_message(filters.text & filters.private & ~filters.command("song") & ~filters.forwarded)
async def text_song(client, message):
    if message.text.startswith("/"):
        return
    text = message.text
    if is_tiktok_url(text) or is_instagram_url(text):
        loading = await message.reply_text("`📥Video yüklənir...`")
        status, path = await loop.run_in_executor(None, download_social_video, text)
        if not path:
            return await loading.edit(status)
        await loading.edit("`📥Video göndərilir...`")
        await message.reply_video(video=path, caption="✅Video uğurla yükləndi")
        return await loading.delete()
        os.remove(path)
    query = text
    url = get_url(query)
    if url:
        mystic = await message.reply_text("`🔍Musiqi axtarılır...`")
        result = await loop.run_in_executor(None, get_yt_info_query, url)
        if not result:
            return await mystic.edit("❌Musiqi tapılmadı")
        title, duration_min, thumb, videoid, link = result
        if str(duration_min) == "None" or duration_min == 0:
            return await mystic.edit("❌Canlı musiqiləri yükləmək olmur")
        await mystic.delete()
        buttons = song_markup(videoid, message.from_user.id)
        return await message.reply_photo(photo=thumb, caption=f"📎**Adı**: [{title}]({link})\n\n⏳**Müddəti**: `{duration_min}`", reply_markup=buttons)
    mystic = await message.reply_text("`🔍Musiqi axtarılır...`")
    result = await loop.run_in_executor(None, get_yt_info_query, query)
    if not result:
        return await mystic.edit("❌Musiqi tapılmadı")
    title, duration_min, thumb, videoid, link = result
    if str(duration_min) == "None" or duration_min == 0:
        return await mystic.edit("❌Canlı musiqiləri yükləmək olmur")
    await mystic.delete()
    buttons = song_markup(videoid, message.from_user.id)
    return await message.reply_photo(photo=thumb, caption=f"📎**Adı**: [{title}]({link})\n\n⏳**Müddəti**: `{duration_min}`", reply_markup=buttons)

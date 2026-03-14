from pyrogram import filters
from pyrogram.enums import ChatType
from config import OWNER_ID, LOG_GROUP_ID, BOT_ID
from Song.helpers.inline import song_markup, start_markup, group_markup, help_markup, help_cb_markup
from Song.helpers.song import get_yt_info_query
from database import add_served_user, add_served_chat, remove_served_chat
from Song import app, loop


@app.on_message(filters.command("start") & ~filters.forwarded)
@app.on_edited_message(filters.command("start") & ~filters.forwarded)
async def start(client, message):
    if message.chat.type == ChatType.PRIVATE:
        if len(message.text.split()) > 1:
            cmd = message.text.split(None, 1)[1]
            if cmd[0:3] == "inf":
                videoid = cmd.replace("info_", "", 1)
                try:
                    await message.delete()
                except:
                    pass
                url = f"https://youtu.be/{videoid}"
                mystic = await message.reply_text("`🔍Musiqi axtarılır...`")
                result = await loop.run_in_executor(None, get_yt_info_query, url)
                if result:
                    title, duration_min, thumb, videoid, link = result
                    if str(duration_min) == "None":
                        return await mystic.edit("❌Canlı musiqiləri yükləmək olmur")
                    await mystic.delete()
                    buttons = song_markup(videoid, message.from_user.id)
                    return await message.reply_photo(photo=thumb, caption=f"📎**Adı**: [{title}]({link})\n\n⏳**Müddəti**: {duration_min}", reply_markup=buttons)
                else:
                    return await mystic.edit("❌Musiqi tapılmadı")
        else:
            await message.reply_text(f"👋Salam {message.from_user.mention}\n\nℹ️**Mən musiqi yükləmək üçün hazırlanmış botam**\n\n✅İstifadə qaydasını öyrənmək üçün əmrlər bölməsinə daxil olun", reply_markup=start_markup)
            await app.send_message(LOG_GROUP_ID, f"👤{message.from_user.mention} botu başlatdı\n\n**🆔ID:** `{message.from_user.id}`")
            return await add_served_user(message.from_user.id)
    else:
        await message.reply_text(f"👋Salam {message.from_user.mention} bot aktivdir\n\n🎵Musiqi yükləmək üçün /song əmrindən istifadə edə bilərsiniz\n\n🆘Hər hansı bir problemlə qarşılaşsanız botun kömək qrupunda soruşa bilərsiniz", reply_markup=group_markup)
        await app.send_message(LOG_GROUP_ID, f"💡 {message.from_user.mention} `{message.chat.title}` qrupunda botu başlatdı")
        return await add_served_chat(message.chat.id)


@app.on_callback_query(filters.regex("cbstart"))
async def cbstart(client, query):
    await query.edit_message_text(f"👋Salam {query.from_user.mention}\n\nℹ️**Mən musiqi yükləmək üçün hazırlanmış botam**\n\n✅İstifadə qaydasını öyrənmək üçün əmrlər bölməsinə daxil olun", reply_markup=start_markup)


@app.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(f"🎵Musiqi yükləmək üçün həm /song əmrindən istifadə edərək, həm də musiqi adını və ya YouTube linkini göndərərək, yükləyə bilərsiniz\n\n🔍Axtarış etmək üçün /search əmrindən istifadə edə bilərsiniz\n\n**⚠️Botun qruplarda normal işləyə bilməsi üçün admin olmalıdır**", reply_markup=help_markup)


@app.on_callback_query(filters.regex("cbhelp"))
async def help_cb(client, query):
    await query.edit_message_text(f"🎵Musiqi yükləmək üçün həm /song əmrindən istifadə edərək, həm də musiqi adını və ya YouTube linkini göndərərək, yükləyə bilərsiniz\n\n🔍Axtarış etmək üçün /search əmrindən istifadə edə bilərsiniz\n\n**⚠️Botun qruplarda işləyə bilməsi üçün admin olmalıdır**", reply_markup=help_cb_markup)


@app.on_message(filters.command("alive") & filters.user(OWNER_ID))
async def alive(client, message):
    await message.reply_text("`😎Mən əla işləyirəm`")


@app.on_message(filters.command("send") & filters.private & filters.user(OWNER_ID))
async def send(client, message):
    command_parts = message.text.split(maxsplit=2)
    id = command_parts[1]
    text = command_parts[2]
    try:
        await app.send_message(id, text)
        await message.reply("✅Mesaj göndərildi")
    except Exception as e:
        await message.reply(f"❌Xəta baş verdi: {str(e)}")


@app.on_message(filters.new_chat_members)
async def welcome(client, message):
    for new_user in message.new_chat_members:
        if str(new_user.id) == str(BOT_ID):
            count = await app.get_chat_members_count(message.chat.id)
            if message.from_user:
                await message.reply(f"👋Salam {message.from_user.mention} məni `{message.chat.title}` qrupuna əlavə etdiyiniz üçün təşəkkürlər🥰")
                await app.send_message(LOG_GROUP_ID, f"🚀 {message.from_user.mention} məni `{message.chat.title}` qrupuna əlavə etdi\n\n💡Qrup üzvlərinin sayı: {count}")
            else:
                await message.reply(f"👋Salam, məni `{message.chat.title}` qrupuna əlavə etdiyiniz üçün təşəkkürlər🥰")
                await app.send_message(LOG_GROUP_ID, f"🚀Mən `{message.chat.title}` qrupuna əlavə edildim\n\n💡Qrup üzvlərinin sayı: {count}")
            await add_served_chat(message.chat.id)


@app.on_message(filters.left_chat_member)
async def leave(client, message):
    if message.left_chat_member.id == BOT_ID:
        if message.from_user:
            await app.send_message(LOG_GROUP_ID, f"🥺 {message.from_user.mention} məni `{message.chat.title}` qrupundan çıxartdı")
        else:
            await app.send_message(LOG_GROUP_ID, f"🥺Mən `{message.chat.title}` qrupundan çıxarıldım")
        await remove_served_chat(message.chat.id)

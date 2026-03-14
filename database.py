from typing import Dict, List, Union
from motor.motor_asyncio import AsyncIOMotorClient


db = AsyncIOMotorClient("mongodb+srv://Huseyn1999:Huseyn1999@cluster0.mcimmcl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongodb = db.Bot
db1 = AsyncIOMotorClient("mongodb+srv://Huseyn1999:Huseyn1999@cluster0.mcimmcl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongodb1 = db1.Bot
chats = mongodb1.chats
users = mongodb1.users
premium = mongodb1.premium
music = mongodb.music


async def is_served_user(user_id: int) -> bool:
    user = await users.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in users.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await users.insert_one({"user_id": user_id})


async def remove_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return await users.delete_one({"user_id": user_id})
    return


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chats.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chats.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chats.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return await chats.delete_one({"chat_id": chat_id})
    return
    

async def get_premium() -> list:
    chats_list = []
    async for chat in premium.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_premium(chat_id: int) -> bool:
    chat = await premium.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_premium(chat_id: int):
    is_served = await is_premium(chat_id)
    if is_served:
        return
    return await premium.insert_one({"chat_id": chat_id})


async def remove_premium(chat_id: int):
    is_served = await is_premium(chat_id)
    if is_served:
        return await premium.delete_one({"chat_id": chat_id})
    return


async def check(title):
    existing_music = await music.find_one({"title": title})
    if not existing_music:
        await music.insert_one({"title": title})
        return True
    else:
        return False

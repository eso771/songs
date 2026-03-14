import asyncio
from pyrogram import Client
from config import *
from .logging import LOGGER

loop = asyncio.get_event_loop()


app = Client("Song", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

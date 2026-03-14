import asyncio
import importlib
import sys
from pyrogram import idle
from Song import LOGGER, app
from Song.plugins import ALL_MODULES


loop = asyncio.get_event_loop()


async def init():
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Song.plugins." + all_module)
    LOGGER("Song.plugins").info("Successfully Imported Modules")
    LOGGER("Song").info("Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("Song").info("Stopping Bot! GoodBye")

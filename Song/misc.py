import socket
import time

import heroku3
from pyrogram import filters

from cinfig import Config
from Song.core.mongo import mongodb

from .logging import LOGGER

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(Cinfig.HEROKU_API_KEY),
    "https",
    str(Cinfig.HEROKU_APP_NAME),
    "HEAD",
    "master",
]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"Local Database Initialized.")


async def sudo():
    global SUDOERS
    SUDOERS.add(Cinfig.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(cinfig.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info(f"Sudoers Loaded.")


def heroku():
    global HAPP
    if is_heroku:
        if Cinfig.HEROKU_API_KEY and Cinfig.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(Cinfig.HEROKU_API_KEY)
                HAPP = Heroku.app(Cinfig.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"Heroku App Configured")
            except BaseException:
                LOGGER(__name__).warning(
                    f"Please make sure your Heroku API Key and Your App name are configured correctly in the heroku."
                )

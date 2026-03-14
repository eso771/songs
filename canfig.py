import re
import random
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()
BANNED_USERS = filters.user()




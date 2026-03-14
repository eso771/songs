import os
import re
import random
from dotenv import load_dotenv
from pyrogram import filters


OWNER_IDS = [8493825254]
OWNER_ID = 8493825254
MONGO_URL = "mongodb+srv://agautevdragitevsvh:pJSptT6jE0pcw9a4@cluster0.de4uc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
BANNED_USERS = filters.user()

class Config:

    OWNER_ID = int(os.getenv("OWNER_ID", "7426096650"))
    OWNER_NAME = os.getenv("OWNER_NAME", "AxtarmaTagYoxdu")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://agautevdragitevsvh:pJSptT6jE0pcw9a4@cluster0.de4uc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "HRKU-AAdPH7_nWkFVf8RyVBkkCjtONJc7sbRbCacmP7eUTOcA_____wOZSRzZHeuk")
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "xmusic")

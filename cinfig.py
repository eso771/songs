import os
import re
import random
from dotenv import load_dotenv
from pyrogram import filters


MONGO_URL = "mongodb+srv://agautevdragitevsvh:pJSptT6jE0pcw9a4@cluster0.de4uc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
  

class Config:

    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://agautevdragitevsvh:pJSptT6jE0pcw9a4@cluster0.de4uc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

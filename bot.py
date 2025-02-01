import asyncio
from pyrogram import Client, compose,idle
import os

from plugins.cb_data import app as Client2

TOKEN = os.environ.get("TOKEN", "7857832326:AAEelUaX96QkzWzj-NmPXP418LF_MqUbNPA")

API_ID = int(os.environ.get("API_ID", "24817837"))

API_HASH = os.environ.get("API_HASH", "acd9f0cc6beb08ce59383cf250052686")

STRING = os.environ.get("STRING", "")


bot = Client(

           "Renamer",

           bot_token=TOKEN,

           api_id=API_ID,

           api_hash=API_HASH,

           plugins=dict(root='plugins'))
           

if STRING:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()

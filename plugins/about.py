import os 
from pyrogram import Client, filters
token = os.environ.get('TOKEN','7857832326:AAEelUaX96QkzWzj-NmPXP418LF_MqUbNPA')
botid = token.split(':')[0]
from helper.database import botdata, find_one, total_user
from helper.progress import humanbytes
@Client.on_message(filters.private & filters.command(["about"]))
async def start(client,message):
	botdata(int(botid))
	data = find_one(int(botid))
	total_rename = data["total_rename"]
	total_size = data["total_size"]
	await message.reply_text(f"Total User:- {total_user()}\nBot :-[Ultra renamer bot](http://t.me/Ultra_renamer_bot)\nCreateur** :- @Kingcey**\nLanguage :-Python3\nLibrary :- Pyrogram 2.0\nServer :- Railway\nFichier Total renommé :-{total_rename}\nPoids Total :- {humanbytes(int(total_size))} ",quote=True)

import os
import pymongo
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
import humanize
from helper.progress import humanbytes
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size, usertype, backpre
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import add_date, check_expi
import datetime
from datetime import date as date_

CHANNEL = os.environ.get('CHANNEL', "")
STRING = os.environ.get("STRING", "")
log_channel = int(os.environ.get("LOG_CHANNEL", ""))
token = os.environ.get('TOKEN', '')
botid = token.split(':')[0]

DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["promo"]

def profind(id):
    return dbcol.find_one({"_id": id})

# Détermination du moment de la journée
currentTime = datetime.datetime.now()

if currentTime.hour < 12:
    wish = "Bonjour."
elif 12 <= currentTime.hour < 18:
    wish = 'Bon après-midi.'
else:
    wish = 'Bonsoir.'

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    old = insert(int(message.chat.id))
    user_id = message.from_user.id
    letdata = profind(int(user_id))
    try:
        procode = letdata["promo"]
    except:
        pass
    try:
        id = message.text.split(' ')[1]
    except:
        await message.reply_text(text=f"""
{wish} {message.from_user.first_name}  
__Je suis un bot de renommage de fichiers.  
Veuillez m'envoyer un **Document ou une Vidéo**  
et entrez un nouveau nom de fichier pour le renommer.__
""", reply_to_message_id=message.id,
reply_markup=InlineKeyboardMarkup(
[[InlineKeyboardButton("Support 🇮🇳", url="https://t.me/lntechnical")],
[InlineKeyboardButton("S'abonner 🧐", url="https://youtube.com/c/LNtechnical")]]))
        return
    if id:
        if id == procode:
            await message.reply_text("Vous pouvez maintenant utiliser le service.")
            uploadlimit(int(user_id), 10737418240)
            usertype(int(user_id), "NORMAL")

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = CHANNEL
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            await message.reply_text("**__Vous n'êtes pas abonné à mon canal__**",
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Support 🇮🇳", url=f"https://t.me/{update_channel}")]]))
            return
    try:
        bot_data = find_one(int(botid))
        prrename = bot_data['total_rename']
        prsize = bot_data['total_size']
        user_deta = find_one(user_id)
    except:
        await message.reply_text("Utilisez d'abord la commande /about")
        return
    try:
        used_date = user_deta["date"]
        buy_date = user_deta["prexdate"]
        daily = user_deta["daily"]
        user_type = user_deta["usertype"]
    except:
        await message.reply_text("La base de données a été réinitialisée. Cliquez sur /start")
        return

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 600
        await message.reply_text(f"Complétez la tâche et obtenez un abonnement gratuit par jour. Regardez la vidéo complète : https://lntechnical.works/{message.from_user.id}")
        return
    elif user_type == "NORMAL":
        LIMIT = 250
    else:
        LIMIT = 30
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"```Désolé, je ne suis pas uniquement disponible pour vous. \nLe contrôle des inondations est actif, veuillez attendre {ltime}```", reply_to_message_id=message.id)
    else:
        await client.forward_messages(log_channel, message.from_user.id, message.id)
        await client.send_message(log_channel, f"ID utilisateur : {user_id}")

        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
            if user_type == "NORMAL":
                usertype(message.from_user.id, "Free")

        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"Désolé ! Je ne peux pas téléverser des fichiers de plus de {humanbytes(limit)}. Taille du fichier détectée : {humanbytes(file.file_size)}\nLimite quotidienne utilisée : {humanbytes(used)}. Si vous voulez renommer un fichier plus grand, mettez à niveau votre plan.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Mettre à niveau 💰💳", callback_data="upgrade")]]))
            return
        if value < file.file_size:
            if STRING:
                if buy_date is None:
                    await message.reply_text(f"Vous ne pouvez pas téléverser plus de {humanbytes(limit)}. Limite quotidienne utilisée : {humanbytes(used)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Mettre à niveau 💰💳", callback_data="upgrade")]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check:
                    await message.reply_text(f"""__Que voulez-vous faire avec ce fichier ?__\n**Nom du fichier** : {filename}\n**Taille du fichier** : {humanize.naturalsize(file.file_size)}\n**Dc ID** : {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Renommer", callback_data="rename"), InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]]))
                    total_rename(int(botid), prrename)
                    total_size(int(botid), prsize, file.file_size)
                else:
                    backpre(message.from_user.id)
                    await message.reply_text(f"Votre abonnement a expiré le {buy_date}", quote=True)
                    return
            else:
                await message.reply_text("Impossible de téléverser des fichiers de plus de 2 Go")
                return
        else:
            filesize = humanize.naturalsize(file.file_size)
            await message.reply_text(f"""__Que voulez-vous faire avec ce fichier ?__\n**Nom du fichier** : {filename}\n**Taille du fichier** : {filesize}\n**Dc ID** : {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Renommer", callback_data="rename"), InlineKeyboardButton("✖️ Annuler", callback_data="cancel")]]))

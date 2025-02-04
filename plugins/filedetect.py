from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        media = await client.get_messages(message.chat.id, message.reply_to_message.id)
        file = media.reply_to_message.document or media.reply_to_message.video or media.reply_to_message.audio
        filename = file.file_name
        types = file.mime_type.split("/")
        mime = types[0]
        mg_id = media.reply_to_message.id
        try:
            out = new_name.split(".")
            out[1]
            out_name = out[-1]
            out_filename = new_name
            await message.reply_to_message.delete()
            if mime == "video":
                markup = InlineKeyboardMarkup([[ 
                InlineKeyboardButton("📁 Document", callback_data="doc"), 
                InlineKeyboardButton("🎥 Vidéo", callback_data="vid") ]])
            elif mime == "audio":
                markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document", callback_data="doc"),
                InlineKeyboardButton("🎵 Audio", callback_data="aud") ]])
            else:
                markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document", callback_data="doc") ]])
            # Ne modifiez pas ce message.reply_text      
            await message.reply_text(f"**Sélectionnez le type de fichier de sortie**\n**Nom du fichier de sortie** :- ```{out_filename}```", 
            reply_to_message_id=mg_id, reply_markup=markup)
            
        except:
            try:
                out = filename.split(".")
                out_name = out[-1]
                out_filename = new_name + "." + out_name
            except:
                await message.reply_to_message.delete()
                await message.reply_text("**Erreur** : Aucune extension dans le fichier, non supporté",
                reply_to_message_id=mg_id)
                return
            await message.reply_to_message.delete()
            if mime == "video":
                markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document", callback_data="doc"),
                InlineKeyboardButton("🎥 Vidéo", callback_data="vid") ]])
            elif mime == "audio":
                markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document", callback_data="doc"),
                InlineKeyboardButton("🎵 Audio", callback_data="aud") ]])
            else:
                markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📁 Document", callback_data="doc") ]])
            # Ne modifiez pas ce message.reply_text 
            await message.reply_text(f"**Sélectionnez le type de fichier de sortie**\n**Nom du fichier de sortie** :- ```{out_filename}```",
            reply_to_message_id=mg_id, reply_markup=markup)

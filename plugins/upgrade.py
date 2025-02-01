from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from pyrogram import Client, filters

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot, update):
	text = """**Utilisateur du Plan Gratuit**  
	Limite de téléversement quotidienne : 2GB  
	Prix : 0F
	
	**VIP 1**  
	Limite de téléversement quotidienne : 50GB  
	Prix :  2000F / 🌎 $ par an  
	
	**VIP 2**  
	Limite de téléversement quotidienne : Illimitée  
	Prix :  3500F / 🌎 $ par an  
	
	Payez par Mobile Money : ```payer par numéro de téléphone```  
	
	Après le paiement, envoyez la capture d'écran  
        du paiement à l'Administrateur."""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("ADMIN 🛂", url="https://t.me/Kingcey")], 
        			[InlineKeyboardButton("PayPal 🌎", url="https://www.paypal.me"),
        			InlineKeyboardButton("Paytm", url="https://p.paytm.me")],
        			[InlineKeyboardButton("Annuler", callback_data="cancel")]])
	await update.message.edit(text=text, reply_markup=keybord)
	

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot, message):
	text = """**Utilisateur du Plan Gratuit**  
	Limite de téléversement quotidienne : 2GB  
	Prix : 0  
	
	**VIP 1**  
	Limite de téléversement quotidienne : 50GB  
	Prix :  2000F  / 🌎 $ par an  
	
	**VIP 2**  
	Limite de téléversement quotidienne : Illimitée  
	Prix : 3500F / 🌎 $ par an  
	
	Payez en utilisant l'UPI ID : ```9480251952@paytm```  
	
	Après le paiement, envoyez la capture d'écran  
        du paiement à l'Administrateur."""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("ADMIN 🛂", url="https://t.me/Kingcey")], 
        			[InlineKeyboardButton("PayPal 🌎", url="https://www.paypal.me"),
        			InlineKeyboardButton("Paytm", url="https://p.paytm.me")],
        			[InlineKeyboardButton("Annuler", callback_data="cancel")]])
	await message.reply_text(text=text, reply_markup=keybord)

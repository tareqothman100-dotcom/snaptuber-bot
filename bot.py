import os
import telebot

# تأكد أن الاسم بين القوسين هو نفس الاسم في Railway
TOKEN = os.environ.get("BOT_TOKEN") 

if TOKEN is None:
    raise ValueError("BOT_TOKEN غير موجود! تأكد من إضافته في إعدادات Railway")

bot = telebot.TeleBot(TOKEN)

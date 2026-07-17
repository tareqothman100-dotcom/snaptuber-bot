

import os
import telebot
from telebot import types
import yt_dlp

# الحصول على التوكن من متغيرات البيئة
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# معرف البوت الخاص بك
BOT_USERNAME = "@snaptuber_bot"

# معرف قناتك التي يجب الاشتراك فيها
CHANNEL_ID = "@wa3yteb" 

# دالة التحقق من اشتراك المستخدم
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"أهلاً بك في {BOT_USERNAME}! أرسل لي رابط الفيديو وسأقوم بمساعدتك في تحميله.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    user_id = message.from_user.id
    url = message.text

    # التحقق من الاشتراك
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك في القناة الآن", url="https://t.me/wa3yteb")
        markup.add(btn)
        bot.reply_to(message, "⚠️ عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:", reply_markup=markup)
        return

    # عملية التحميل
    if "http" in url:
        try:
            bot.reply_to(message, "⏳ جاري المعالجة والتحميل، يرجى الانتظار...")
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove('video.mp4')
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ أثناء التحميل: {str(e)}")
    else:
        bot.reply_to(message, "❌ يرجى إرسال رابط صحيح.")

print("Bot is running...")
bot.infinity_polling()

import os
import telebot
import yt_dlp

# قراءة التوكن من المتغيرات في Railway
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط الفيديو وسأقوم بمساعدتك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "http" in url:
        try:
            bot.reply_to(message, "جاري المعالجة...")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video.mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            os.remove('video.mp4')
            
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {str(e)}")
    else:
        bot.reply_to(message, "يرجى إرسال رابط صحيح.")

# استخدام infinity_polling لضمان استقرار الاتصال على السيرفر
bot.infinity_polling()

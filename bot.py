import logging
import os
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
from flask import Flask
from threading import Thread

# إعداد السيرفر الوهمي
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    app_web.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# إعدادات البوت
TOKEN = os.environ.get("TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ جاري التحميل ... انتظر قليلاً.")
    
    # إنشاء اسم ملف فريد (مثل: 550e8400-e29b-41d4-a716-446655440000.mp4)
    unique_filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {'format': 'best', 'outtmpl': unique_filename}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الملف الفريد
        await update.message.reply_video(video=open(unique_filename, 'rb'))
        
        # حذف الملف بعد الإرسال لتنظيف السيرفر
        os.remove(unique_filename)
        
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

if __name__ == '__main__':
    # تشغيل السيرفر في الخلفية
    Thread(target=run_web).start()
    
    # تشغيل البوت
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()

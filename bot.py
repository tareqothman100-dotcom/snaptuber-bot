import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.environ.get("TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
url = update.message.text
await update.message.reply_text("⏳ جاري التحميل... انتظر قليلاً.")

ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
try:
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
ydl.download([url])
await update.message.reply_video(video=open('video.mp4', 'rb'))
except Exception as e:
await update.message.reply_text(f"خطأ: {e}")

if name == 'main':
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
app.run_polling()
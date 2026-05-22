import os
import yt_dlp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8961367759:AAFpF2RVCIvYZu27Zn-boWZIyW5Wo5csCA0"

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("📥 Descargando video...")

    opciones = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])

        archivo = None

        for f in os.listdir():
            if f.startswith("video."):
                archivo = f
                break

        if archivo:
            await update.message.reply_video(video=open(archivo, 'rb'))

            os.remove(archivo)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, descargar)
)

print("Bot activo 🚀")
app.run_polling()


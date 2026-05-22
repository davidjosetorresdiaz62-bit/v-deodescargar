from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import yt_dlp
import os

TOKEN = "8961367759:AAFpF2RVCIvYZu27Zn-boWZIyW5Wo5csCA0"

# ========= MENÚ PRINCIPAL =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
🎬 <b>BOT DOWNLOADER PRO</b>

✨ Descarga videos fácilmente desde:

• YouTube
• TikTok
• Facebook
• Instagram

📥 Solo envía un enlace.
"""

    botones = [
        [
            InlineKeyboardButton("🎥 Descargar Video", callback_data="video")
        ],
        [
            InlineKeyboardButton("🎵 Descargar MP3", callback_data="mp3")
        ],
        [
            InlineKeyboardButton("👑 Créditos", callback_data="creditos")
        ]
    ]

    teclado = InlineKeyboardMarkup(botones)

    await update.message.reply_text(
        texto,
        parse_mode="HTML",
        reply_markup=teclado
    )

# ========= BOTONES =========

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "video":

        context.user_data["modo"] = "video"

        await query.message.reply_text(
            "📥 Envía el enlace del video"
        )

    elif query.data == "mp3":

        context.user_data["modo"] = "mp3"

        await query.message.reply_text(
            "🎵 Envía el enlace para descargar audio"
        )

    elif query.data == "creditos":

        await query.message.reply_text(
            "✨ Bot creado con Python + Telegram"
        )

# ========= DESCARGAS =========

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    modo = context.user_data.get("modo", "video")

    await update.message.reply_text(
        "⏳ Procesando descarga..."
    )

    try:

        if modo == "video":

            opciones = {
                "format": "mp4",
                "outtmpl": "video.%(ext)s"
            }

        else:

            opciones = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])

        # ========= ENVIAR VIDEO =========

        if modo == "video":

            archivo = None

            for f in os.listdir():
                if f.startswith("video."):
                    archivo = f
                    break

            if archivo:

                await update.message.reply_video(
                    video=open(archivo, "rb"),
                    caption="✅ Descarga completada"
                )

                os.remove(archivo)

        # ========= ENVIAR AUDIO =========

        else:

            archivo = None

            for f in os.listdir():
                if f.endswith(".mp3"):
                    archivo = f
                    break

            if archivo:

                await update.message.reply_audio(
                    audio=open(archivo, "rb"),
                    caption="🎵 MP3 listo"
                )

                os.remove(archivo)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )

# ========= INICIAR BOT =========

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(botones))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        descargar
    )
)

print("🚀 Bot elegante activo")

app.run_polling()

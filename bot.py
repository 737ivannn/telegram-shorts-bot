import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram.constants import ChatAction

BOT_TOKEN = os.getenv("BOT_TOKEN") or "paste-your-token-here"

VIDEO_DIR = "videos"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send /short to get a random short video.")

async def short(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4") or f.endswith(".mov")]
    if not files:
        await update.message.reply_text("No videos found.")
        return

    chosen = random.choice(files)
    video_path = os.path.join(VIDEO_DIR, chosen)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
    await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, "rb"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("short", short))

    app.run_polling()

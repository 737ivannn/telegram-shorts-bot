import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7963868497:AAFsgZHqtsTaIDXP0wNsx0ogYSQAUQslE8M"
VIDEO_FOLDER = "videos"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Next 🎥", callback_data="next")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click below to get a video.", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    video_files = os.listdir(VIDEO_FOLDER)
    if not video_files:
        await query.message.reply_text("No videos available.")
        return
    video_path = os.path.join(VIDEO_FOLDER, random.choice(video_files))
    keyboard = [[InlineKeyboardButton("Next 🎥", callback_data="next")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_video(chat_id=query.message.chat_id, video=open(video_path, 'rb'), reply_markup=reply_markup)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Bot is running...")
    app.run_polling()

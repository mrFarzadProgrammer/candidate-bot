# super_simple_bot.py
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیمات
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8327912063:AAEh4Q_mrVsAl9GYiSLTnQH-Cg251RxCyCY')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("سلام بات!", callback_data="hello")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! من کار می‌کنم 🎉", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ بات فعال است!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("🚀 بات اجرا شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
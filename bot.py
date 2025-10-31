# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# توکن بات
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8327912063:AAEh4Q_mrVsAl9GYiSLTnQH-Cg251RxCyCY')

# آیدی نماینده
REPRESENTATIVE_ID = 96763697

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دستور /start
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("معرفی کاندید", callback_data="candidate_info")],
        [InlineKeyboardButton("عکس‌ها", callback_data="photos")],
        [InlineKeyboardButton("رزومه", callback_data="resume")],
        [InlineKeyboardButton("ایده‌ها", callback_data="ideas")],
        [InlineKeyboardButton("آدرس ستادها", callback_data="addresses")],
        [InlineKeyboardButton("ارتباط با من", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🌟 به بات کاندید خوش آمدید!\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup
    )

# مدیریت دکمه‌ها
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "candidate_info":
        candidate_text = "👨‍💼 **معرفی کاندید:**\n📌 نام: علی رضایی"
        query.edit_message_text(candidate_text)
    elif query.data == "photos":
        query.edit_message_text("📸 بخش عکس‌ها")
    elif query.data == "resume":
        query.edit_message_text("📄 رزومه کاری")
    elif query.data == "ideas":
        query.edit_message_text("💡 ایده‌ها و برنامه‌ها")
    elif query.data == "addresses":
        query.edit_message_text("📍 آدرس ستادها")
    elif query.data == "contact":
        query.edit_message_text("📞 ارتباط با من")
    elif query.data == "main_menu":
        start(update, context)

def text_handler(update: Update, context: CallbackContext):
    update.message.reply_text("✅ پیام شما دریافت شد.")

def photo_handler(update: Update, context: CallbackContext):
    update.message.reply_text("✅ عکس دریافت شد.")

def voice_handler(update: Update, context: CallbackContext):
    update.message.reply_text("✅ ویس دریافت شد.")

def error_handler(update: Update, context: CallbackContext):
    logger.error(f"Update caused error: {context.error}")

# تابع راه‌اندازی بات
def setup_bot():
    """راه‌اندازی بات تلگرام"""
    try:
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CallbackQueryHandler(button_handler))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
        dp.add_handler(MessageHandler(Filters.photo, photo_handler))
        dp.add_handler(MessageHandler(Filters.voice, voice_handler))
        dp.add_error_handler(error_handler)
        
        logger.info("🤖 بات تلگرام راه‌اندازی شد...")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")

# سرور HTTP ساده
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Bot is running!</h1></body></html>')
    
    def log_message(self, format, *args):
        logger.info(f"HTTP: {format % args}")

def run_http_server():
    """راه‌اندازی سرور HTTP"""
    PORT = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', PORT), SimpleHandler)
    logger.info(f"🌐 سرور HTTP اجرا شد روی پورت {PORT}")
    server.serve_forever()

def main():
    """تابع اصلی"""
    logger.info("🚀 شروع برنامه...")
    
    # راه‌اندازی بات در thread جداگانه
    bot_thread = threading.Thread(target=setup_bot, daemon=True)
    bot_thread.start()
    logger.info("🧵 بات در thread جداگانه راه‌اندازی شد")
    
    # راه‌اندازی سرور HTTP در thread اصلی
    run_http_server()

if __name__ == '__main__':
    main()
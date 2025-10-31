# -*- coding: utf-8 -*-
import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

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

# 🔹 تمام توابع شما دقیقاً مثل قبل - فقط async هستند
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("معرفی کاندید", callback_data="candidate_info")],
        [InlineKeyboardButton("عکس‌ها", callback_data="photos")],
        [InlineKeyboardButton("رزومه", callback_data="resume")],
        [InlineKeyboardButton("ایده‌ها", callback_data="ideas")],
        [InlineKeyboardButton("آدرس ستادها", callback_data="addresses")],
        [InlineKeyboardButton("ارتباط با من", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌟 به بات کاندید خوش آمدید!\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "candidate_info":
        await query.edit_message_text("👨‍💼 **معرفی کاندید:**\n📌 نام: علی رضایی")
    elif query.data == "photos":
        await query.edit_message_text("📸 بخش عکس‌ها")
    elif query.data == "resume":
        await query.edit_message_text("📄 رزومه کاری")
    elif query.data == "ideas":
        await query.edit_message_text("💡 ایده‌ها و برنامه‌ها")
    elif query.data == "addresses":
        await query.edit_message_text("📍 آدرس ستادها")
    elif query.data == "contact":
        await query.edit_message_text("📞 ارتباط با من")
    elif query.data == "main_menu":
        await start(update, context)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ پیام شما دریافت شد.")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ عکس دریافت شد.")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ویس دریافت شد.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update caused error: {context.error}")

# 🔹 تابع اصلی برای Render
async def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_error_handler(error_handler)
        
        # 🔹 روی Render باید از webhook استفاده کنیم
        PORT = int(os.environ.get('PORT', 10000))
        
        # ساخت یک سرور ساده HTTP روی پورت مورد نظر
        from aiohttp import web
        
        async def handle(request):
            return web.Response(text="Bot is running!")
        
        app = web.Application()
        app.router.add_get('/', handle)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, '0.0.0.0', PORT)
        await site.start()
        
        logger.info(f"✅ سرور اجرا شد روی پورت {PORT}")
        
        # اجرای بات با polling (در پس‌زمینه)
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        logger.info("✅ بات شروع به کار کرد!")
        
        # نگه داشتن برنامه در حال اجرا
        while True:
            await asyncio.sleep(3600)
            
    except Exception as e:
        logger.error(f"خطا: {e}")

# 🔹 راه حل جایگزین: فقط یک سرور HTTP ساده
def simple_server():
    """یک سرور ساده که Render راضی کند"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Bot is running!')
        
        def log_message(self, format, *args):
            logger.info(f"HTTP: {format % args}")
    
    def run_bot():
        """اجرای بات در یک thread جداگانه"""
        try:
            application = Application.builder().token(BOT_TOKEN).build()
            
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CallbackQueryHandler(button_handler))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
            application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
            application.add_handler(MessageHandler(filters.VOICE, voice_handler))
            application.add_error_handler(error_handler)
            
            logger.info("🤖 بات در حال اجرا...")
            application.run_polling()
        except Exception as e:
            logger.error(f"خطا در بات: {e}")
    
    # اجرای بات در background
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # اجرای سرور HTTP
    PORT = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    logger.info(f"🌐 سرور HTTP اجرا شد روی پورت {PORT}")
    server.serve_forever()

if __name__ == '__main__':
    # استفاده از راه حل ساده‌تر
    simple_server()
# -*- coding: utf-8 -*-
import os
import logging
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن بات
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8327912063:AAEh4Q_mrVsAl9GYiSLTnQH-Cg251RxCyCY')

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    await update.message.reply_text("🌟 به بات کاندید خوش آمدید!", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ بات فعال است!")

async def handle_webhook(request):
    """دریافت پیام‌های وب‌هوک از تلگرام"""
    try:
        data = await request.json()
        update = Update.de_json(data, request.app['bot'])
        await request.app['application'].process_update(update)
        return web.Response(text="OK")
    except Exception as e:
        logger.error(f"خطا در پردازش وب‌هوک: {e}")
        return web.Response(status=400)

async def health_check(request):
    """بررسی سلامت"""
    return web.Response(text="Bot is running!")

async def init_app():
    """راه‌اندازی برنامه"""
    # ساخت اپلیکیشن تلگرام
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    await application.initialize()
    await application.start()
    
    # ساخت اپلیکیشن aiohttp
    app = web.Application()
    app['bot'] = application.bot
    app['application'] = application
    
    # مسیرها
    app.router.add_post(f'/{BOT_TOKEN}', handle_webhook)
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    return app

if __name__ == '__main__':
    # راه‌اندازی سرور
    PORT = int(os.environ.get('PORT', 10000))
    web.run_app(init_app(), host='0.0.0.0', port=PORT)
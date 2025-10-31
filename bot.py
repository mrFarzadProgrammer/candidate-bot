# -*- coding: utf-8 -*-
import os
import logging
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

# دستور /start
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

# مدیریت دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "candidate_info":
        candidate_text = "👨‍💼 **معرفی کاندید:**\n📌 نام: علی رضایی"
        await query.edit_message_text(candidate_text)
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

async def main():
    """تابع اصلی با وب‌هوک واقعی"""
    try:
        # ساخت اپلیکیشن
        application = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_error_handler(error_handler)
        
        # تنظیمات وب‌هوک برای Render
        PORT = int(os.environ.get('PORT', 10000))
        RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL', f'http://localhost:{PORT}')
        
        logger.info(f"🚀 راه‌اندازی بات روی {RENDER_URL}")
        
        # تنظیم وب‌هوک
        await application.bot.set_webhook(
            url=f"{RENDER_URL}/{BOT_TOKEN}",
            drop_pending_updates=True
        )
        
        # راه‌اندازی سرور وب‌هوک
        await application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=RENDER_URL,
            secret_token="WEBHOOK_SECRET"
        )
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
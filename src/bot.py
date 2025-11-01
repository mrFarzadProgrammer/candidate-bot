# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# توکن بات اصلی
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8327912063:AAEh4Q_mrVsAl9GYiSLTnQH-Cg251RxCyCY')
REPRESENTATIVE_ID = 96763697

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 تمام توابع شما دقیقاً مثل dev_bot.py می‌مونن
# [start, candidate_callback, photos_callback, resume_callback, 
#  ideas_callback, addresses_callback, contact_callback, button_handler, 
#  text_handler, photo_handler, voice_handler, error_handler]

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

# 🔹 بقیه توابع رو دقیقاً از dev_bot.py کپی کن...

def main():
    """تابع اصلی - دو حالت: اگر آدرس HTTPS داشتیم وب‌هوک، وگرنه پولینگ"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_error_handler(error_handler)
        
        PORT = int(os.environ.get('PORT', 10000))
        WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_URL', '')
        
        # 🔹 تشخیص حالت اجرا
        if WEBHOOK_URL and WEBHOOK_URL.startswith('https://'):
            # حالت Production - Webhook
            logger.info(f"🚀 اجرا با وب‌هوک روی: {WEBHOOK_URL}")
            
            application.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=BOT_TOKEN,
                webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
                drop_pending_updates=True
            )
        else:
            # حالت Fallback - Polling (مثل توسعه)
            logger.info("🔧 اجرا با پولینگ (حالت Fallback)")
            logger.info("📱 بات اصلی آماده دریافت پیام...")
            
            application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")

if __name__ == '__main__':
    main()
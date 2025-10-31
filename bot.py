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

# تمام توابع قبلی شما بدون تغییر می‌مونن...
# [همان توابع start, candidate_callback, photos_callback, etc.]

def main():
    try:
        # ساخت اپلیکیشن
        application = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        application.add_error_handler(error_handler)
        
        # بررسی محیط اجرا
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER') or os.environ.get('PORT'):
            # محیط production - استفاده از webhook
            PORT = int(os.environ.get('PORT', 8080))
            WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')  # باید در متغیرهای محیطی ست شود
            
            if WEBHOOK_URL:
                await application.run_webhook(
                    listen="0.0.0.0",
                    port=PORT,
                    url_path=BOT_TOKEN,
                    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
                )
            else:
                # اگر WEBHOOK_URL ست نشده، روی پورت اجرا شود
                application.run_webhook(
                    listen="0.0.0.0",
                    port=PORT,
                    url_path="",
                    webhook_url=""
                )
                logger.info(f"✅ Bot running on port {PORT} in production mode")
        else:
            # محیط development - استفاده از polling
            logger.info("✅ بات در حالت توسعه شروع به کار کرد...")
            application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
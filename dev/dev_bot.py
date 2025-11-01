# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 🔹 توکن بات تست تو
DEV_BOT_TOKEN = os.environ.get('DEV_BOT_TOKEN', '8204524746:AAGBAf7OhMaMPXud3hObuGZYR-BCzdTMiPo')

# آیدی نماینده (همان)
REPRESENTATIVE_ID = 96763697

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧪 تست منوی اصلی", callback_data="test_main")],
        [InlineKeyboardButton("🚀 ویژگی جدید", callback_data="new_feature")],
        [InlineKeyboardButton("🐛 تست خطا", callback_data="test_error")],
        [InlineKeyboardButton("📊 آمار توسعه", callback_data="dev_stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🧪 **بات توسعه - Saman Test Bot**\n\n"
        "این نسخه برای تست ویژگی‌های جدید است\n"
        "هر تغییری اینجا تست می‌شود\n"
        "نسخه اصلی: @CandidateMainBot",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "test_main":
        await query.edit_message_text(
            "✅ **تست منوی اصلی موفق**\n\n"
            "این پیام نشان می‌دهد بات به درستی کار می‌کند\n"
            "می‌توانید ویژگی‌های جدید را اضافه کنید"
        )
    elif query.data == "new_feature":
        await query.edit_message_text(
            "🚀 **ویژگی جدید توسعه**\n\n"
            "این یک ویژگی آزمایشی است\n"
            "پس از تست کامل به نسخه اصلی منتقل می‌شود"
        )
    elif query.data == "test_error":
        try:
            # تست خطا
            raise Exception("این یک خطای تستی است")
        except Exception as e:
            await query.edit_message_text(f"🐛 **خطای تست:** {e}")
    elif query.data == "dev_stats":
        user = query.from_user
        await query.edit_message_text(
            f"📊 **آمار توسعه**\n\n"
            f"👤 کاربر: {user.first_name}\n"
            f"🆔 آیدی: {user.id}\n"
            f"📱 حالت: توسعه\n"
            f"✅ بات تست فعال"
        )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧪 **پیام دریافت شد (توسعه)**\n\n"
        "این پاسخ از نسخه توسعه است\n"
        "ویژگی‌های جدید اینجا تست می‌شوند"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"خطا در توسعه: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            f"🐛 **خطا در توسعه:**\n{context.error}\n\n"
            "این خطا فقط در نسخه تست نشان داده می‌شود"
        )

def main():
    """بات توسعه - فقط برای تست"""
    try:
        application = Application.builder().token(DEV_BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        application.add_error_handler(error_handler)
        
        logger.info("🧪 بات توسعه اجرا شد...")
        logger.info("📱 به @saman_rahjou_test_bot پیام بدهید")
        logger.info("🚀 می‌توانید ویژگی‌های جدید را تست کنید")
        
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات توسعه: {e}")

if __name__ == '__main__':
    main()
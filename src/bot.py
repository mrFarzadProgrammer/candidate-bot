# -*- coding: utf-8 -*-
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# توکن بات اصلی
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8327912063:AAEh4Q_mrVsAl9GYiSLTnQH-Cg251RxCyCY')

# آیدی نماینده
REPRESENTATIVE_ID = 96763697

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تمام توابع اصلی
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

# 🔹 بقیه توابع رو دقیقاً از کد قبلی کپی کن اینجا
# [candidate_callback, photos_callback, resume_callback, ideas_callback, 
#  addresses_callback, contact_callback, button_handler, text_handler, 
#  photo_handler, voice_handler, error_handler]

async def candidate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    candidate_text = """
👨‍💼 **معرفی کاندید:**

📌 نام و نام خانوادگی: علی رضایی
📅 تاریخ تولد: ۱۵ فروردین ۱۳۶۵
🎓 تحصیلات:
  • دکترای مهندسی کامپیوتر - دانشگاه تهران
  • کارشناسی ارشد مدیریت کسب و کار - دانشگاه شریف
"""
    await query.edit_message_text(candidate_text)
    await show_back_button(query, context)

async def show_back_button(query, context):
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="برای بازگشت به منوی اصلی از دکمه زیر استفاده کنید:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "candidate_info":
            await candidate_callback(update, context)
        elif query.data == "photos":
            await photos_callback(update, context)
        elif query.data == "resume":
            await resume_callback(update, context)
        elif query.data == "ideas":
            await ideas_callback(update, context)
        elif query.data == "addresses":
            await addresses_callback(update, context)
        elif query.data == "contact":
            await contact_callback(update, context)
        elif query.data == "main_menu":
            await show_main_menu(update, context)
    except Exception as e:
        logger.error(f"Error in button_handler: {e}")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("معرفی کاندید", callback_data="candidate_info")],
        [InlineKeyboardButton("عکس‌ها", callback_data="photos")],
        [InlineKeyboardButton("رزومه", callback_data="resume")],
        [InlineKeyboardButton("ایده‌ها", callback_data="ideas")],
        [InlineKeyboardButton("آدرس ستادها", callback_data="addresses")],
        [InlineKeyboardButton("ارتباط با من", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "منوی اصلی - لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )

# هندلرهای ساده برای متن، عکس و ویس
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ پیام شما دریافت شد.")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ عکس دریافت شد.")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ویس دریافت شد.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update caused error: {context.error}")

def main():
    """تابع اصلی - بدون aiohttp"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن هندلرها
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
        application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_error_handler(error_handler)
        
        # اجرا با وب‌هوک ساده
        PORT = int(os.environ.get('PORT', 10000))
        
        logger.info(f"🚀 بات اصلی اجرا شد روی پورت {PORT}")
        
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url="",  # خالی بذار
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")

if __name__ == '__main__':
    main()
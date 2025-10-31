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
    try:
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
        logger.info(f"User {update.message.from_user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start command: {e}")

# توابع callback برای دکمه‌ها
async def candidate_callback(query, context):
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

async def photos_callback(query, context):
    try:
        photo_urls = [
            "https://picsum.photos/400/300",
            "https://picsum.photos/400/301"
        ]
        
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_urls[0],
            caption="عکس رسمی کاندید"
        )
        
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_urls[1],
            caption="عکس در محیط کاری"
        )
        
        await show_back_button_after_photos(query, context)
        
    except Exception as e:
        logger.error(f"Error in photos_callback: {e}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ خطا در دریافت عکس‌ها"
        )

async def show_back_button_after_photos(query, context):
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="برای بازگشت به منوی اصلی از دکمه زیر استفاده کنید:",
        reply_markup=reply_markup
    )

async def resume_callback(query, context):
    resume_text = """
📄 **رزومه کاری**
    
💼 سوابق شغلی:
• مدیر عامل شرکت فناوری اطلاعات نوآور - ۱۴۰۰ تاکنون
• مشاور ارشد فناوری اطلاعات - ۱۳۹۶-۱۴۰۰
    
🏆 دستاوردها:
• راه‌اندازی ۵ استارت‌آپ موفق
• دریافت جایزه بهترین مدیر جوان
"""
    await query.edit_message_text(resume_text)
    await show_back_button(query, context)

async def ideas_callback(query, context):
    ideas_text = """
💡 **ایده‌ها و برنامه‌ها**
    
🎯 چشم‌انداز توسعه فناوری:
• تبدیل شهر به قطب استارت‌آپ‌ها
• هوشمندسازی خدمات شهری
    
🌱 برنامه‌های اقتصادی:
• حمایت از کسب‌وکارهای کوچک
• جذب سرمایه‌گذاری خارجی
"""
    await query.edit_message_text(ideas_text)
    await show_back_button(query, context)

async def addresses_callback(query, context):
    addresses_text = """
📍 **آدرس ستادهای انتخاباتی**
    
🏢 ستاد مرکزی:
تهران، خیابان ولیعصر، پلاک ۱۰۰۰
تلفن: ۰۲۱-۱۲۳۴۵۶۷۸
    
🏢 ستاد منطقه ۱:
تهران، میدان ونک، خیابان ملاصدرا
"""
    await query.edit_message_text(addresses_text)
    await show_back_button(query, context)

async def contact_callback(query, context):
    contact_text = """
📞 **ارتباط با من**

شما می‌توانید پیام خود را در قالب متن، عکس یا ویس ارسال کنید.

📝 **دستورالعمل:**
1. پیام خود را ارسال کنید
2. برای پایان و ارسال نهایی، از دکمه "پایان و ارسال" استفاده کنید

پیام شما مستقیماً برای نماینده ارسال خواهد شد.
"""
    
    keyboard = [
        [InlineKeyboardButton("پایان و ارسال", callback_data="finish_contact")],
        [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ذخیره وضعیت کاربر برای دریافت پیام
    context.user_data['waiting_for_contact'] = True
    context.user_data['contact_messages'] = []
    
    await query.edit_message_text(
        contact_text,
        reply_markup=reply_markup
    )

async def show_back_button(query, context):
    keyboard = [[InlineKeyboardButton("بازگشت به منوی اصلی", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="برای بازگشت به منوی اصلی از دکمه زیر استفاده کنید:",
        reply_markup=reply_markup
    )

async def show_main_menu(query, context):
    keyboard = [
        [InlineKeyboardButton("معرفی کاندید", callback_data="candidate_info")],
        [InlineKeyboardButton("عکس‌ها", callback_data="photos")],
        [InlineKeyboardButton("رزومه", callback_data="resume")],
        [InlineKeyboardButton("ایده‌ها", callback_data="ideas")],
        [InlineKeyboardButton("آدرس ستادها", callback_data="addresses")],
        [InlineKeyboardButton("ارتباط با من", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # پاک کردن وضعیت کاربر
    if 'waiting_for_contact' in context.user_data:
        del context.user_data['waiting_for_contact']
    if 'contact_messages' in context.user_data:
        del context.user_data['contact_messages']
    
    await query.edit_message_text(
        "منوی اصلی - لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def finish_contact(query, context):
    user = query.from_user
    
    if 'contact_messages' in context.user_data and context.user_data['contact_messages']:
        try:
            # ارسال اطلاعات کاربر به نماینده
            user_info = f"""
👤 **پیام جدید از کاربر:**

🆔 آیدی: {user.id}
👤 نام: {user.first_name} {user.last_name or ''}
📱 یوزرنیم: @{user.username or 'ندارد'}

📨 محتوای پیام:
"""
            await context.bot.send_message(chat_id=REPRESENTATIVE_ID, text=user_info)
            
            # ارسال پیام‌های کاربر به نماینده
            for msg_type, content in context.user_data['contact_messages']:
                if msg_type == 'text':
                    await context.bot.send_message(chat_id=REPRESENTATIVE_ID, text=f"📝 متن کاربر:\n{content}")
                elif msg_type == 'photo':
                    await context.bot.send_photo(chat_id=REPRESENTATIVE_ID, photo=content, caption="📸 عکس ارسالی کاربر")
                elif msg_type == 'voice':
                    await context.bot.send_voice(chat_id=REPRESENTATIVE_ID, voice=content, caption="🎤 ویس ارسالی کاربر")
            
            # پاک کردن داده‌ها
            del context.user_data['contact_messages']
            del context.user_data['waiting_for_contact']
            
            await query.edit_message_text(
                "✅ پیام شما با موفقیت ارسال شد!\n\n"
                "از اینکه نظر خود را با ما در میان گذاشتید سپاسگزاریم.\n"
                "پاسخ شما در اسرع وقت داده خواهد شد."
            )
            
        except Exception as e:
            logger.error(f"Error sending contact messages: {e}")
            await query.edit_message_text("⚠️ خطا در ارسال پیام")
    else:
        await query.edit_message_text(
            "⚠️ هیچ پیامی برای ارسال وجود ندارد.\n\n"
            "لطفاً ابتدا پیام خود را ارسال کنید سپس بر روی دکمه 'پایان و ارسال' کلیک کنید."
        )

# مدیریت کلیک روی دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "candidate_info":
            await candidate_callback(query, context)
        elif query.data == "photos":
            await photos_callback(query, context)
        elif query.data == "resume":
            await resume_callback(query, context)
        elif query.data == "ideas":
            await ideas_callback(query, context)
        elif query.data == "addresses":
            await addresses_callback(query, context)
        elif query.data == "contact":
            await contact_callback(query, context)
        elif query.data == "main_menu":
            await show_main_menu(query, context)
        elif query.data == "finish_contact":
            await finish_contact(query, context)
    except Exception as e:
        logger.error(f"Error in button_handler: {e}")

# مدیریت دریافت پیام‌های متنی
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_contact', False):
        # ذخیره پیام متنی
        if 'contact_messages' not in context.user_data:
            context.user_data['contact_messages'] = []
        
        context.user_data['contact_messages'].append(('text', update.message.text))
        
        await update.message.reply_text(
            "✅ متن شما دریافت شد.\n"
            "می‌توانید پیام دیگری ارسال کنید یا بر روی 'پایان و ارسال' کلیک کنید."
        )

# مدیریت دریافت عکس
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_contact', False):
        # ذخیره عکس
        if 'contact_messages' not in context.user_data:
            context.user_data['contact_messages'] = []
        
        photo = update.message.photo[-1]  # بزرگترین سایز
        context.user_data['contact_messages'].append(('photo', photo.file_id))
        
        await update.message.reply_text(
            "✅ عکس شما دریافت شد.\n"
            "می‌توانید پیام دیگری ارسال کنید یا بر روی 'پایان و ارسال' کلیک کنید."
        )

# مدیریت دریافت پیام صوتی
async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_contact', False):
        # ذخیره ویس
        if 'contact_messages' not in context.user_data:
            context.user_data['contact_messages'] = []
        
        voice = update.message.voice
        context.user_data['contact_messages'].append(('voice', voice.file_id))
        
        await update.message.reply_text(
            f"✅ ویس شما دریافت شد.\n"
            f"مدت زمان: {voice.duration} ثانیه\n"
            f"می‌توانید پیام دیگری ارسال کنید یا بر روی 'پایان و ارسال' کلیک کنید."
        )
    else:
        # حالت قدیمی برای ویس
        try:
            voice = update.message.voice
            user = update.message.from_user
            
            await update.message.reply_text(
                f"✅ پیام صوتی شما دریافت شد!\n"
                f"مدت زمان: {voice.duration} ثانیه\n"
                f"پیام برای نماینده ارسال خواهد شد."
            )
            
            # ارسال ویس به نماینده
            await context.bot.send_voice(
                chat_id=REPRESENTATIVE_ID,
                voice=voice.file_id,
                caption=f"🎤 ویس از کاربر: {user.first_name} (ID: {user.id})"
            )
            
        except Exception as e:
            logger.error(f"Error in voice_handler: {e}")

# مدیریت خطا
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update caused error: {context.error}")

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
        
        # اجرای بات
        logger.info("✅ بات نماینده شروع به کار کرد...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    main()
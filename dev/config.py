import os
from dotenv import load_dotenv

# لود فایل محیطی توسعه
load_dotenv('dev/.env.dev')

class Config:
    # توکن‌ها
    DEV_BOT_TOKEN = os.getenv('DEV_BOT_TOKEN', '8204524746:AAGBAf7OhMaMPXud3hObuGZYR-BCzdTMiPo')
    PROD_BOT_TOKEN = os.getenv('PROD_BOT_TOKEN', '8327912063:AAEh4Q_mrVsAl9GYiSLTnQH-Cg251RxCyCY')
    
    # تنظیمات
    REPRESENTATIVE_ID = int(os.getenv('REPRESENTATIVE_ID', 96763697))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def is_development():
        return os.getenv('ENVIRONMENT') == 'development'
    
    @staticmethod
    def get_bot_token():
        if Config.is_development():
            return Config.DEV_BOT_TOKEN
        return Config.PROD_BOT_TOKEN
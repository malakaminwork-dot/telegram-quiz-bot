import os

class Config:
    # سيتم تعيين هذه من متغيرات البيئة
    BOT_TOKEN = os.getenv('8117038726:AAFEWJ8H1JyEZu6OGkwehp6LdE9K057-3FQ', '')
    ADMIN_IDS = list(map(int, os.getenv('8422436251', '').split(','))) if os.getenv('ADMIN_IDS') else []
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///quizzes.db')

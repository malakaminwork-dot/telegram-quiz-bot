import os

class Config:
    # سيتم تعيين هذه من متغيرات البيئة
    BOT_TOKEN = os.getenv('8440625760:AAEW7YOKF7vwXp7tBFci3Pp2tYEp6O9AyCk', '')
    ADMIN_IDS = list(map(int, os.getenv('8422436251', '').split(','))) if os.getenv('ADMIN_IDS') else []
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///quizzes.db')

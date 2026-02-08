import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import Config

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("👨‍🏫 أنا مدرس", callback_data='teacher')],
        [InlineKeyboardButton("👨‍🎓 أنا طالب", callback_data='student')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"مرحباً {user.full_name}! 👋\n\n"
        "أهلاً بك في نظام الاختبارات التعليمية\n"
        "اختر هويتك:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'teacher':
        keyboard = [
            [InlineKeyboardButton("📝 إنشاء اختبار", callback_data='create_quiz')],
            [InlineKeyboardButton("📊 رؤية النتائج", callback_data='view_results')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "مرحباً أيها المدرس! 🎓\n\n"
            "اختر المهمة التي تريد تنفيذها:",
            reply_markup=reply_markup
        )
    
    elif query.data == 'student':
        keyboard = [
            [InlineKeyboardButton("📝 الاختبارات المتاحة", callback_data='available_quizzes')],
            [InlineKeyboardButton("📈 نتائجي", callback_data='my_results')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "مرحباً أيها الطالب! 📚\n\n"
            "اختر ما تريد القيام به:",
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 **مساعدة**\n\n"
        "للأسئلة الشائعة:\n"
        "• /start - بدء البوت\n"
        "• /help - هذه الرسالة\n"
        "• /quiz - رؤية الاختبارات\n\n"
        "للتواصل مع الدعم: @support"
    )

def main():
    # إنشاء التطبيق
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # بدء البوت
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

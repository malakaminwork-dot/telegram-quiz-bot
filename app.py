from flask import Flask, jsonify
import os
import threading
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

# تمكين التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== وظائف بوت تلجرام ==========
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رد على أمر /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"🎉 **مرحباً {user.first_name}!**\n\n"
        "أهلاً بك في بوت الاختبارات التعليمية!\n\n"
        "✅ **البوت يعمل بنجاح الآن!**\n\n"
        "👨‍🏫 **للمدرسين:**\n"
        "- إنشاء اختبارات\n- رؤية النتائج\n\n"
        "👨‍🎓 **للطلاب:**\n"
        "- أداء الاختبارات\n- رؤية الدرجات\n\n"
        "🚀 ابدأ باستخدام الأزرار!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رد على أمر /help"""
    await update.message.reply_text(
        "🆘 **مساعدة سريعة:**\n\n"
        "• /start - بدء البوت\n"
        "• /help - هذه الرسالة\n"
        "• /quiz - قريباً: الاختبارات\n\n"
        "📞 للمساعدة: @دعم_البوت"
    )

def run_telegram_bot():
    """تشغيل بوت تلجرام في خيط منفصل"""
    try:
        token = os.getenv('BOT_TOKEN')
        
        if not token:
            logger.error("❌ BOT_TOKEN غير مضبوط!")
            return
        
        logger.info("🤖 بدء تشغيل بوت تلجرام...")
        
        # اختبار التوكن أولاً
        test_url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(test_url, timeout=10)
        
        if not response.json().get('ok'):
            logger.error(f"❌ التوكن خاطئ: {response.json()}")
            return
        
        logger.info("✅ التوكن صحيح، جاري تشغيل البوت...")
        
        # إنشاء وتشغيل البوت
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        
        logger.info("✅ البوت يعمل وجاهز للرسائل!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ خطأ في البوت: {e}")

# ========== صفحات الويب ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Telegram Quiz Bot</title><meta charset="utf-8">
    <style>body{font-family:Arial; padding:40px; text-align:center;}
    .success{background:#4CAF50; color:white; padding:20px; border-radius:10px;}
    </style></head>
    <body>
        <div class="success">
            <h1>✅ البوت يعمل بنجاح!</h1>
            <p>الخدمة: quiz-bot-final-q6sq.onrender.com</p>
            <p>اذهب إلى Telegram وجرب:</p>
            <p><strong>@banktest22bot</strong></p>
            <p>وأرسل: <code>/start</code></p>
        </div>
        <p><a href="/bot-status">📊 حالة البوت</a></p>
    </body>
    </html>
    """

@app.route('/bot-status')
def bot_status():
    """صفحة لعرض حالة البوت"""
    token = os.getenv('BOT_TOKEN')
    status = "❌ غير مفعل"
    
    if token:
        try:
            response = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=5)
            if response.json().get('ok'):
                status = "✅ يعمل وجاهز"
        except:
            status = "⚠️ خطأ في الاتصال"
    
    return jsonify({
        "bot": "@banktest22bot",
        "status": status,
        "service": "quiz-bot-final-q6sq.onrender.com"
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    # تشغيل بوت تلجرام في الخلفية
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    logger.info("🚀 بدء تشغيل البوت في الخلفية...")
    
    # تشغيل خادم Flask
    port = int(os.getenv('PORT', 10000))
    logger.info(f"🌐 بدء خادم الويب على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

from flask import Flask, request, jsonify
import os
import logging
import sys
from threading import Thread
import time

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)
app = Flask(__name__)

# بوت تلجرام مبسط للبدء
def run_simple_bot():
    """تشغيل نسخة مبسطة من البوت"""
    try:
        token = os.getenv('BOT_TOKEN')
        
        if not token or token == 'ضع_توكن_البوت_هنا':
            logger.warning("⚠️ BOT_TOKEN غير مضبوط، البوت لن يعمل")
            logger.info("🔧 يرجى تعيين BOT_TOKEN في إعدادات Render")
            return
        
        logger.info(f"🤖 بدء تشغيل البوت باستخدام التوكن: {token[:10]}...")
        
        # استيراد مكتبة telegram بعد التحقق من التوكن
        try:
            from telegram import Update
            from telegram.ext import Application, CommandHandler, CallbackContext
        except ImportError as e:
            logger.error(f"❌ خطأ في استيراد المكتبات: {e}")
            logger.info("📦 جاري تثبيت المكتبات المطلوبة...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
            from telegram import Update
            from telegram.ext import Application, CommandHandler, CallbackContext
        
        # دالة البداية
        async def start_command(update: Update, context: CallbackContext):
            await update.message.reply_text(
                '🎓 **مرحباً بكم في نظام الاختبارات التعليمية!**\n\n'
                '✅ البوت يعمل بنجاح على Render\n\n'
                '📝 قم بتعديل الكود لإضافة المميزات:\n'
                '1. إنشاء اختبارات\n'
                '2. إدارة الطلاب\n'
                '3. عرض النتائج\n\n'
                '🚀 ابدأ الآن بتجربة البوت!'
            )
        
        # إنشاء وتشغيل البوت
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", start_command))
        
        logger.info("🔄 بدء الاستماع للرسائل...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}", exc_info=True)

# صفحة البداية
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Telegram Quiz Bot",
        "version": "1.0.0",
        "endpoints": {
            "/": "هذه الصفحة",
            "/health": "فحص حالة الخدمة",
            "/start": "بدء البوت (يدوياً)",
            "/bot-status": "حالة البوت"
        },
        "instructions": {
            "1": "اضبط BOT_TOKEN في Environment Variables",
            "2": "أعد تشغيل الخدمة",
            "3": "تفقد السجلات للتحقق من التشغيل"
        }
    })

# فحص الحالة
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "bot_token_set": bool(os.getenv('BOT_TOKEN')),
        "environment": os.getenv('RENDER', 'development')
    })

# بدء البوت يدوياً
@app.route('/start-bot')
def start_bot():
    try:
        bot_thread = Thread(target=run_simple_bot, daemon=True)
        bot_thread.start()
        return jsonify({
            "success": True,
            "message": "✅ تم بدء تشغيل البوت في الخلفية",
            "thread": "running"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# حالة البوت
@app.route('/bot-status')
def bot_status():
    token = os.getenv('BOT_TOKEN')
    return jsonify({
        "bot_configured": bool(token and token != 'ضع_توكن_البوت_هنا'),
        "token_length": len(token) if token else 0,
        "environment": dict(os.environ) if os.getenv('RENDER_EXTERNAL_HOSTNAME') else "غير معروفة"
    })

# تشغيل البوت تلقائياً عند البدء
@app.before_first_request
def initialize():
    logger.info("🚀 تهيئة التطبيق...")
    logger.info(f"📁 المسار: {os.getcwd()}")
    logger.info(f"🐍 إصدار Python: {sys.version}")
    
    # بدء البوت تلقائياً
    if os.getenv('AUTO_START_BOT', 'true').lower() == 'true':
        logger.info("🤖 بدء تشغيل البوت تلقائياً...")
        bot_thread = Thread(target=run_simple_bot, daemon=True)
        bot_thread.start()

# نقطة الدخول الرئيسية
if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    host = '0.0.0.0'
    
    logger.info(f"🌐 تشغيل الخادم على {host}:{port}")
    logger.info("📞 للتحقق: https://telegram-quiz-bot.onrender.com")
    
    app.run(host=host, port=port, debug=False)

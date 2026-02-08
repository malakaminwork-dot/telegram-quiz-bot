from flask import Flask, jsonify
import os
import sys
import subprocess
import time

app = Flask(__name__)

# ========== تثبيت المكتبات المطلوبة ==========
def install_telegram_bot():
    """تثبيت مكتبة python-telegram-bot إذا كانت ناقصة"""
    print("🔍 فحص مكتبات Python...")
    
    try:
        # محاولة استيراد المكتبة
        import telegram
        print("✅ مكتبة telegram مثبتة بالفعل")
        return True
    except ImportError:
        print("📦 جاري تثبيت python-telegram-bot...")
        try:
            # تثبيت المكتبة
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7", "requests==2.31.0"])
            print("✅ تم تثبيت المكتبات بنجاح")
            return True
        except Exception as e:
            print(f"❌ فشل تثبيت المكتبات: {e}")
            return False

# تثبيت المكتبات عند البدء
install_telegram_bot()

# ========== تشغيل بوت Telegram ==========
def start_telegram_bot():
    """بدء تشغيل بوت Telegram بعد تثبيت المكتبات"""
    print("🤖 محاولة تشغيل بوت Telegram...")
    time.sleep(3)  # انتظار للتثبيت
    
    try:
        # الآن حاول استيراد المكتبات بعد التثبيت
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
        import asyncio
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ BOT_TOKEN غير مضبوط")
            return
        
        print(f"✅ التوكن: {token[:10]}...")
        
        # دالة /start
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🎉 **مرحباً! البوت يعمل الآن!**\n\n"
                "✨ **الأوامر المتاحة:**\n"
                "• /start - بدء البوت\n"
                "• /teacher - وضع المدرس\n"
                "• /student - وضع الطالب\n"
                "• /help - المساعدة\n\n"
                "🚀 جرب الآن!"
            )
        
        # دالة /teacher
        async def teacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🏫 **وضع المدرس**\n\n"
                "مميزات المدرس:\n"
                "1. 📝 إنشاء اختبارات جديدة\n"
                "2. 📋 إدارة الاختبارات\n"
                "3. 📊 رؤية نتائج الطلاب\n\n"
                "🚀 سيتم تفعيل هذه المميزات قريباً!"
            )
        
        # دالة /student
        async def student_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🎓 **وضع الطالب**\n\n"
                "مميزات الطالب:\n"
                "1. 📝 رؤية الاختبارات المتاحة\n"
                "2. 🧑‍🎓 أداء الاختبارات\n"
                "3. 🏆 رؤية النتائج\n\n"
                "🚀 سيتم تفعيل هذه المميزات قريباً!"
            )
        
        # دالة /help
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🆘 **مساعدة البوت**\n\n"
                "• /start - بدء البوت\n"
                "• /teacher - دخول وضع المدرس\n"
                "• /student - دخول وضع الطالب\n"
                "• /help - هذه الرسالة\n\n"
                "📞 للمساعدة: @مالك"
            )
        
        # تشغيل البوت
        async def run_bot():
            application = Application.builder().token(token).build()
            application.add_handler(CommandHandler("start", start_command))
            application.add_handler(CommandHandler("teacher", teacher_command))
            application.add_handler(CommandHandler("student", student_command))
            application.add_handler(CommandHandler("help", help_command))
            
            print("✅ بوت Telegram جاهز!")
            print("📞 الأوامر: /start, /teacher, /student, /help")
            
            await application.initialize()
            await application.start()
            await application.updater.start_polling()
            
            # إبقاء البوت يعمل
            print("🎉 بوت Telegram يعمل بنجاح!")
            await asyncio.Event().wait()
        
        # تشغيل في loop جديد
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
        
    except ImportError as e:
        print(f"❌ لا تزال المكتبات ناقصة: {e}")
        print("🔄 إعادة محاولة التثبيت...")
        time.sleep(5)
        if install_telegram_bot():
            start_telegram_bot()  # إعادة المحاولة
    except Exception as e:
        print(f"❌ خطأ في البوت: {e}")

# ========== صفحات الويب ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><title>بوت الاختبارات</title>
<style>
body{font-family:Arial; padding:40px; text-align:center; background:#f0f8ff;}
.container{max-width:700px; margin:0 auto; background:white; padding:40px; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,0.1);}
h1{color:#2c3e50;}
.status-box{padding:20px; margin:20px 0; border-radius:10px; font-weight:bold; font-size:1.2em;}
.installing{background:#ffc107; color:#856404;}
.ready{background:#28a745; color:white;}
.command{display:inline-block; background:#e7f3ff; padding:10px 20px; margin:8px; border-radius:8px; font-family:monospace;}
.btn{padding:15px 30px; margin:15px; background:#0088cc; color:white; text-decoration:none; border-radius:10px; font-weight:bold; display:inline-block;}
</style></head>
<body>
<div class="container">
    <h1>🤖 بوت الاختبارات التعليمية</h1>
    
    <div class="status-box installing">
        🔄 <strong>جاري تثبيت مكتبات البوت...</strong>
    </div>
    
    <p>يتم الآن تثبيت مكتبة python-telegram-bot تلقائياً</p>
    
    <h3>📋 الأوامر المتاحة بعد التثبيت:</h3>
    <div class="command">/start</div>
    <div class="command">/teacher</div>
    <div class="command">/student</div>
    <div class="command">/help</div>
    
    <div style="margin:30px 0;">
        <a href="https://t.me/banktest22bot" class="btn" target="_blank">
            📲 افتح البوت على Telegram
        </a>
        <a href="/check-status" class="btn" style="background:#28a745;">
            🔍 تحقق من الحالة
        </a>
    </div>
    
    <div style="background:#f8f9fa; padding:20px; border-radius:10px; margin-top:30px;">
        <p><strong>⏱ المعلومة:</strong> قد يستغرق التثبيت 30-60 ثانية</p>
        <p>بعدها سيعمل البوت تلقائياً</p>
    </div>
</div>
</body>
</html>
    """

@app.route('/check-status')
def check_status():
    """صفحة التحقق من حالة المكتبات"""
    try:
        import telegram
        lib_status = "✅ مثبتة"
    except ImportError:
        lib_status = "❌ غير مثبتة"
    
    return jsonify({
        "telegram_library": lib_status,
        "bot": "@banktest22bot",
        "service": "running",
        "message": "جاري التثبيت التلقائي للمكتبات"
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("🚀 بدء تشغيل تطبيق البوت...")
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 البوت: @banktest22bot")
    
    # بدء بوت Telegram في thread منفصل
    import threading
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    print("✅ بدأ thread البوت (سيحاول تثبيت المكتبات تلقائياً)")
    
    # بدء خادم Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 خادم الويب على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

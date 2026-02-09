from flask import Flask, jsonify
import os
import sys
import subprocess
import time

app = Flask(__name__)

# ========== تثبيت المكتبات إجبارياً ==========
def force_install_packages():
    """تثبيت المكتبات المطلوبة إجبارياً"""
    print("🔧 تثبيت المكتبات المطلوبة إجبارياً...")
    
    packages = [
        "python-telegram-bot==20.7",
        "Flask==2.3.2", 
        "requests==2.31.0",
        "gunicorn==21.2.0"
    ]
    
    for package in packages:
        try:
            print(f"📦 جاري تثبيت {package}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ تم تثبيت {package}")
            else:
                print(f"⚠️ مشكلة في {package}: {result.stderr[:100]}")
                
        except Exception as e:
            print(f"❌ خطأ في تثبيت {package}: {e}")
    
    print("✅ اكتمل تثبيت المكتبات")

# تثبيت المكتبات عند البدء
force_install_packages()

# ========== تشغيل البوت بعد التأكد من المكتبات ==========
def run_telegram_bot():
    """تشغيل بوت Telegram بعد التأكد من المكتبات"""
    print("🤖 محاولة تشغيل بوت Telegram...")
    time.sleep(3)  # انتظار للتثبيت
    
    try:
        # محاولة استيراد المكتبات
        print("📚 جاري استيراد مكتبات Telegram...")
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ BOT_TOKEN غير مضبوط!")
            return
        
        print(f"✅ التوكن: {token[:15]}...")
        
        # اختبار التوكن
        import requests
        try:
            test = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
            if test.json().get('ok'):
                bot_info = test.json()['result']
                print(f"✅ البوت: @{bot_info['username']}")
            else:
                print(f"❌ التوكن غير صالح: {test.json()}")
                return
        except Exception as e:
            print(f"⚠️ خطأ في اختبار التوكن: {e}")
        
        # دوال الرد البسيطة
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🎉 **أهلاً! البوت يعمل الآن!**\n\n"
                "✨ **الأوامر:**\n"
                "• /teacher - وضع المدرس\n"
                "• /student - وضع الطالب\n"
                "• /help - المساعدة\n\n"
                "🚀 جرب الآن!"
            )
        
        async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🏫 **وضع المدرس**\n\n"
                "مميزات قريباً:\n"
                "• إنشاء اختبارات\n"
                "• إدارة الاختبارات\n"
                "• نتائج الطلاب\n\n"
                "🚀 جاري التطوير!"
            )
        
        async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🎓 **وضع الطالب**\n\n"
                "مميزات قريباً:\n"
                "• أداء الاختبارات\n"
                "• رؤية النتائج\n"
                "• متابعة التقدم\n\n"
                "🚀 جاري التطوير!"
            )
        
        async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🆘 **مساعدة**\n\n"
                "الأوامر:\n"
                "• /start - بدء البوت\n"
                "• /teacher - وضع المدرس\n"
                "• /student - وضع الطالب\n"
                "• /help - هذه الرسالة\n\n"
                "🎯 جرب الآن!"
            )
        
        # إنشاء وتشغيل البوت
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("teacher", teacher))
        app.add_handler(CommandHandler("student", student))
        app.add_handler(CommandHandler("help", help_cmd))
        
        print("✅ البوت جاهز! جاري التشغيل...")
        print("📞 أرسل /start إلى @banktest22bot")
        
        # تشغيل البوت
        app.run_polling()
        
    except ImportError as e:
        print(f"❌ لا تزال المكتبات ناقصة: {e}")
        print("🔄 إعادة تثبيت المكتبات...")
        force_install_packages()
        time.sleep(5)
        run_telegram_bot()  # إعادة المحاولة
        
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
body{font-family:Arial; padding:50px; text-align:center; background:#f0f8ff;}
.container{max-width:700px; margin:0 auto; background:white; padding:40px; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,0.1);}
h1{color:#2c3e50;}
.status{padding:20px; margin:20px 0; border-radius:10px; font-size:1.2em; font-weight:bold;}
.installing{background:#ffc107; color:#856404;}
.success{background:#28a745; color:white;}
.btn{padding:15px 30px; margin:15px; background:#0088cc; color:white; text-decoration:none; border-radius:10px; font-weight:bold; display:inline-block;}
.command{display:inline-block; background:#e7f3ff; padding:10px 20px; margin:10px; border-radius:8px; font-family:monospace;}
</style></head>
<body>
<div class="container">
    <h1>🤖 بوت الاختبارات التعليمية</h1>
    
    <div class="status installing">
        🔄 <strong>جاري تثبيت المكتبات إجبارياً...</strong>
    </div>
    
    <p>يتم الآن تثبيت <code>python-telegram-bot</code> تلقائياً</p>
    
    <div style="margin:30px 0;">
        <div class="command">/start</div>
        <div class="command">/teacher</div>
        <div class="command">/student</div>
        <div class="command">/help</div>
    </div>
    
    <div>
        <a href="https://t.me/banktest22bot" class="btn" target="_blank">
            📲 افتح البوت على Telegram
        </a>
        <a href="/force-restart" class="btn" style="background:#28a745;">
            🔄 إعادة تثبيت قسري
        </a>
    </div>
    
    <div style="margin-top:40px; padding:20px; background:#f8f9fa; border-radius:10px; color:#666;">
        <p><strong>💡 معلومة:</strong> التثبيت الإجباري يستغرق 1-2 دقيقة</p>
        <p>بعدها سيعمل البوت تلقائياً</p>
    </div>
</div>
</body>
</html>
"""

@app.route('/force-restart')
def force_restart():
    """إعادة تثبيت وتشغيل البوت"""
    import threading
    thread = threading.Thread(target=run_telegram_bot, daemon=True)
    thread.start()
    return jsonify({
        "status": "restarting",
        "message": "جاري إعادة تثبيت وتشغيل البوت..."
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 بدء تشغيل البوت مع التثبيت الإجباري")
    print("=" * 60)
    
    # بدء البوت في thread منفصل
    import threading
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    print("✅ بدأ تشغيل البوت في الخلفية")
    
    # معلومات التشغيل
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 البوت: @banktest22bot")
    print("📋 الأوامر: /start, /teacher, /student, /help")
    print("=" * 60)
    
    # بدء Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 خادم Flask على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

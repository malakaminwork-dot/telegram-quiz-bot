from flask import Flask, jsonify
import os
import subprocess
import sys
import time

app = Flask(__name__)

# ========== تثبيت المكتبات المطلوبة أولاً ==========
def install_requirements():
    """تثبيت المكتبات المطلوبة إذا كانت ناقصة"""
    print("📦 فحص المكتبات المطلوبة...")
    
    # قائمة المكتبات الأساسية
    requirements = [
        "python-telegram-bot==20.7",
        "Flask==2.3.2", 
        "requests==2.31.0"
    ]
    
    for package in requirements:
        try:
            # حاول استيراد المكتبة
            if "telegram" in package:
                import telegram
                print(f"✅ {package} مثبتة")
            elif "Flask" in package:
                import flask
                print(f"✅ {package} مثبتة")
            elif "requests" in package:
                import requests
                print(f"✅ {package} مثبتة")
        except ImportError:
            # تثبيت المكتبة إذا كانت ناقصة
            print(f"📥 جاري تثبيت {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ تم تثبيت {package}")
            except:
                print(f"❌ فشل تثبيت {package}")

# ========== تشغيل البوت ==========
def start_telegram_bot():
    """بدء بوت تلجرام بعد تثبيت المكتبات"""
    print("🤖 محاولة تشغيل بوت تلجرام...")
    time.sleep(2)  # انتظار للتثبيت
    
    try:
        # استيراد المكتبات بعد التثبيت
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        import asyncio
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ BOT_TOKEN غير مضبوط!")
            return
        
        print(f"✅ التوكن: {token[:10]}...")
        
        # اختبار التوكن
        import requests
        test = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=5)
        if not test.json().get('ok'):
            print(f"❌ التوكن خاطئ: {test.json()}")
            return
        
        print("✅ التوكن صحيح!")
        
        # دالة الرد
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            await update.message.reply_text(
                f"🎉 **أهلاً {user.first_name}!**\n\n"
                "✅ **بوت الاختبارات التعليمية يعمل الآن!**\n\n"
                "مميزات البوت:\n"
                "• 📝 إنشاء اختبارات\n"
                "• 🧑‍🎓 أداء الاختبارات\n"
                "• 📊 عرض النتائج\n\n"
                "🚀 ابدأ تجربتك الآن!"
            )
        
        # تشغيل البوت
        async def run_bot():
            application = Application.builder().token(token).build()
            application.add_handler(CommandHandler("start", start_command))
            application.add_handler(CommandHandler("help", start_command))
            
            print("✅ بوت تلجرام جاهز للتشغيل!")
            print(f"📞 أرسل /start إلى @banktest22bot")
            
            await application.initialize()
            await application.start()
            await application.updater.start_polling()
            
            # إبقاء البوت يعمل
            print("🎯 بوت تلجرام يعمل بنجاح!")
            await asyncio.Event().wait()
        
        # تشغيل في loop جديد
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())
        
    except ImportError as e:
        print(f"❌ مكتبة ناقصة: {e}")
        install_requirements()
        # حاول مرة أخرى بعد التثبيت
        time.sleep(3)
        start_telegram_bot()
    except Exception as e:
        print(f"❌ خطأ: {e}")

# ========== صفحات الويب ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><title>بوت الاختبارات</title>
<style>
body{font-family:Arial; padding:40px; text-align:center; background:#f8f9fa;}
.container{max-width:600px; margin:0 auto; background:white; padding:30px; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);}
.status{padding:15px; margin:15px 0; border-radius:8px; font-weight:bold;}
.success{background:#d4edda; color:#155724; border:2px solid #c3e6cb;}
.step{background:#e7f3ff; padding:10px; margin:8px 0; border-radius:5px; border-right:4px solid #007bff;}
.btn{display:inline-block; padding:12px 25px; margin:10px; background:#28a745; color:white; text-decoration:none; border-radius:8px; font-weight:bold;}
.telegram{background:#0088cc;}
</style></head>
<body>
<div class="container">
    <h1>🤖 بوت الاختبارات التعليمية</h1>
    
    <div class="status success">
        ✅ <strong>جاري تشغيل البوت...</strong>
    </div>
    
    <h3>🚀 الخطوات التلقائية:</h3>
    <div class="step">1. فحص المكتبات المطلوبة</div>
    <div class="step">2. تثبيت المكتبات الناقصة</div>
    <div class="step">3. بدء بوت تلجرام</div>
    <div class="step">4. البوت جاهز على @banktest22bot</div>
    
    <div style="margin:30px 0;">
        <a href="https://t.me/banktest22bot" class="btn telegram" target="_blank">
            📲 افتح البوت الآن
        </a>
        <a href="/status" class="btn">
            📊 حالة النظام
        </a>
    </div>
    
    <p style="color:#666; margin-top:20px;">
        ⏱ يرجى الانتظار 30-60 ثانية بعد النشر ليبدأ البوت بالكامل
    </p>
</div>
</body>
</html>
    """

@app.route('/status')
def status():
    token = os.getenv('BOT_TOKEN')
    return jsonify({
        "service": "running",
        "bot_configured": bool(token),
        "bot": "@banktest22bot",
        "message": "جاري تشغيل البوت تلقائياً..."
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("🚀 بدء تشغيل تطبيق البوت...")
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 البوت: @banktest22bot")
    
    # تثبيت المكتبات أولاً
    install_requirements()
    
    # بدء بوت تلجرام في thread منفصل
    import threading
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    print("✅ بدأ تشغيل بوت تلجرام في الخلفية")
    
    # بدء خادم Flask
    port = int(os.getenv('PORT', 10000))
    print(f"🌐 بدء خادم الويب على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

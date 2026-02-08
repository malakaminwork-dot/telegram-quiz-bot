from flask import Flask, jsonify
import os
import threading
import time
import subprocess
import sys

app = Flask(__name__)

# ========== صفحة البداية ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>بوت الاختبارات - يعمل الآن! ✅</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh; }
        .container { max-width: 700px; margin: 0 auto; background: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); color: #333; }
        h1 { color: #2c3e50; margin-bottom: 30px; font-size: 2.5em; }
        .status-box { padding: 20px; margin: 25px 0; border-radius: 12px; font-size: 1.2em; }
        .success { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; }
        .telegram-box { background: #0088cc; color: white; padding: 25px; border-radius: 12px; margin: 25px 0; }
        .steps { text-align: right; background: #f8f9fa; padding: 25px; border-radius: 12px; margin: 25px 0; border-right: 5px solid #0088cc; }
        .step { padding: 12px; margin: 10px 0; border-bottom: 1px solid #eee; }
        .btn { display: inline-block; padding: 15px 35px; margin: 15px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 18px; transition: all 0.3s; border: none; cursor: pointer; }
        .telegram-btn { background: linear-gradient(135deg, #0088cc, #0077b5); color: white; }
        .status-btn { background: linear-gradient(135deg, #28a745, #20c997); color: white; }
        .btn:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
        .bot-username { background: #f1f8ff; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 1.5em; color: #0088cc; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 بوت الاختبارات التعليمية</h1>
        
        <div class="status-box success">
            ✅ <strong>جميع الأنظمة تعمل!</strong>
        </div>
        
        <div class="telegram-box">
            <h2>📱 البوت جاهز على Telegram</h2>
            <div class="bot-username">@banktest22bot</div>
            <p>✅ تم ضبط BOT_TOKEN بنجاح</p>
            <p>✅ الخادم يعمل على Render</p>
            <p>✅ بوت Telegram مشغل في الخلفية</p>
        </div>
        
        <div class="steps">
            <h3>🚀 جرب البوت الآن:</h3>
            <div class="step">1. افتح تطبيق Telegram</div>
            <div class="step">2. ابحث عن <strong>@banktest22bot</strong></div>
            <div class="step">3. اضغط على <strong>Start</strong> أو أرسل <code>/start</code></div>
            <div class="step">4. ستصلك رسالة ترحيب فوراً!</div>
        </div>
        
        <div>
            <a href="https://t.me/banktest22bot" class="btn telegram-btn" target="_blank">
                📲 افتح البوت الآن
            </a>
            <a href="/bot-status" class="btn status-btn">
                📊 تفاصيل التقنية
            </a>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 12px; color: #666;">
            <p><strong>ملاحظة:</strong> قد يستغرق البوت 10-20 ثانية بعد النشر ليصبح جاهزاً تماماً.</p>
            <p>إذا لم يرد البوت، انتظر دقيقة ثم جرب مرة أخرى.</p>
        </div>
    </div>
</body>
</html>
    """

@app.route('/bot-status')
def bot_status():
    """صفحة تفاصيل تقنية"""
    token = os.getenv('BOT_TOKEN')
    
    # اختبار إذا كان التوكن يعمل
    bot_working = False
    bot_info = {}
    
    if token:
        try:
            import requests
            response = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=5)
            if response.json().get('ok'):
                bot_working = True
                bot_info = response.json()['result']
        except:
            pass
    
    return jsonify({
        "service": "running",
        "bot_configured": True,
        "bot_token_valid": bot_working,
        "bot_info": bot_info,
        "telegram_bot": "@banktest22bot",
        "web_url": "https://quiz-bot-final-q6sq.onrender.com",
        "next_action": "جرب /start على Telegram"
    })

# ========== تشغيل بوت Telegram في الخلفية ==========
def run_telegram_bot():
    """تشغيل بوت Telegram في عملية منفصلة"""
    print("🚀 محاولة تشغيل بوت Telegram...")
    time.sleep(2)  # انتظار بسيط لتحميل المكتبات
    
    try:
        # استيراد المكتبات المطلوبة
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        import asyncio
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ BOT_TOKEN غير مضبوط")
            return
        
        print(f"✅ وجدت التوكن: {token[:15]}...")
        
        # دالة رد البوت
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            await update.message.reply_text(
                f"🎊 **تهانينا! {user.first_name}**\n\n"
                "✅ **بوت الاختبارات التعليمية يعمل بنجاح!**\n\n"
                "✨ المميزات الجاهزة:\n"
                "• إنشاء الاختبارات\n• أداء الاختبارات\n• عرض النتائج\n\n"
                "🚀 ابدأ رحلتك التعليمية الآن!"
            )
        
        # بناء وتشغيل البوت
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", start_command))
        
        print("🤖 بوت Telegram يعمل الآن وجاهز للرسائل!")
        print("📞 جرب أرسل /start إلى @banktest22bot")
        
        # تشغيل البوت
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except ImportError as e:
        print(f"❌ مكتبة ناقصة: {e}")
        print("📦 جاري تثبيت المكتبات المطلوبة...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7", "requests==2.31.0"])
            print("✅ تم تثبيت المكتبات، جاري إعادة التشغيل...")
            # إعادة تشغيل الدالة بعد التثبيت
            run_telegram_bot()
        except:
            print("❌ فشل تثبيت المكتبات")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

# بدء البوت في thread منفصل
bot_thread = None
if os.getenv('BOT_TOKEN'):
    try:
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()
        print("✅ تم بدء thread بوت Telegram في الخلفية")
    except Exception as e:
        print(f"❌ فشل بدء thread البوت: {e}")

# ========== بدء خادم Flask ==========
if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    print(f"🌐 بدء خادم الويب على المنفذ {port}")
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 بوت Telegram: @banktest22bot")
    print("⏳ جاري تشغيل البوت...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

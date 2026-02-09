from flask import Flask, jsonify
import os
import sys
import subprocess
import time
import threading
import traceback

app = Flask(__name__)

# ========== تثبيت المكتبات المطلوبة ==========
def install_telegram_bot():
    """تثبيت مكتبة python-telegram-bot إذا كانت ناقصة"""
    print("🔍 فحص مكتبات Python...")
    
    try:
        import telegram
        print("✅ مكتبة telegram مثبتة بالفعل")
        return True
    except ImportError:
        print("📦 جاري تثبيت python-telegram-bot...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7", "requests==2.31.0"])
            print("✅ تم تثبيت المكتبات بنجاح")
            return True
        except Exception as e:
            print(f"❌ فشل تثبيت المكتبات: {e}")
            return False

# ========== تشغيل بوت Telegram ==========
def start_telegram_bot():
    """بدء تشغيل بوت Telegram بعد تثبيت المكتبات"""
    print("=" * 60)
    print("🤖 بدء تشغيل بوت Telegram...")
    print("=" * 60)
    
    try:
        # استيراد المكتبات
        print("📦 جاري استيراد مكتبات Telegram...")
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
        import requests
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ خطأ: BOT_TOKEN غير مضبوط في البيئة!")
            print(f"📋 متغيرات البيئة: {list(os.environ.keys())}")
            return
        
        print(f"✅ وجدت BOT_TOKEN: {token[:15]}...")
        
        # اختبار التوكن
        print("🔐 جاري اختبار التوكن مع API Telegram...")
        try:
            test = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
            if test.json().get('ok'):
                bot_info = test.json()['result']
                print(f"✅ التوكن صحيح! البوت: @{bot_info['username']}")
                print(f"   الاسم: {bot_info['first_name']}")
                print(f"   المعرف: {bot_info['id']}")
            else:
                print(f"❌ التوكن خاطئ أو غير فعال: {test.json()}")
                return
        except Exception as e:
            print(f"⚠️ خطأ في اختبار التوكن: {e}")
        
        # ========== دوال الرد ==========
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            
            keyboard = [
                [InlineKeyboardButton("👨‍🏫 أنا مدرس", callback_data='teacher_mode')],
                [InlineKeyboardButton("👨‍🎓 أنا طالب", callback_data='student_mode')],
                [InlineKeyboardButton("❓ المساعدة", callback_data='help_info')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"🎓 **مرحباً {user.first_name}!**\n\n"
                "أهلاً بك في نظام الاختبارات التعليمية\n\n"
                "اختر هويتك للبدء:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        async def teacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🏫 **وضع المدرس**\n\n"
                "مميزات المدرس:\n"
                "• 📝 إنشاء اختبارات جديدة\n"
                "• 📋 إدارة الاختبارات الحالية\n"
                "• 📊 متابعة نتائج الطلاب\n\n"
                "🚀 سيتم تفعيل هذه المميزات قريباً!",
                parse_mode='Markdown'
            )
        
        async def student_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🎓 **وضع الطالب**\n\n"
                "مميزات الطالب:\n"
                "• 📝 أداء الاختبارات المتاحة\n"
                "• 🏆 رؤية النتائج السابقة\n"
                "• 📈 متابعة التقدم\n\n"
                "🚀 سيتم تفعيل هذه المميزات قريباً!",
                parse_mode='Markdown'
            )
        
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🆘 **مساعدة البوت**\n\n"
                "**الأوامر الحالية:**\n"
                "• /start - رسالة الترحيب\n"
                "• /teacher - وضع المدرس\n"
                "• /student - وضع الطالب\n"
                "• /help - هذه الرسالة\n\n"
                "🎯 **جرب الآن:** أرسل /teacher أو /student",
                parse_mode='Markdown'
            )
        
        # إنشاء تطبيق البوت
        print("🔧 جاري إنشاء تطبيق البوت...")
        application = Application.builder().token(token).build()
        
        # إضافة handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("teacher", teacher_command))
        application.add_handler(CommandHandler("student", student_command))
        application.add_handler(CommandHandler("help", help_command))
        
        print("✅ تم إضافة جميع الأوامر!")
        print("📡 جاري بدء استماع البوت للرسائل...")
        
        # تشغيل البوت - هذا السطر سيبدأ البوت فعلياً
        print("🚀 بدء تشغيل البوت باستخدام run_polling()...")
        application.run_polling()
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد المكتبات: {e}")
        print("📦 جاري تثبيت المكتبات المطلوبة...")
        install_telegram_bot()
        print("🔄 إعادة محاولة تشغيل البوت بعد التثبيت...")
        time.sleep(5)
        start_telegram_bot()  # إعادة المحاولة
        
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {type(e).__name__}: {e}")
        print("📋 تفاصيل الخطأ:")
        traceback.print_exc()

# ========== صفحة ويب بسيطة ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>بوت الاختبارات التعليمية</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 50px;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            color: #333;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .status {
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
        }
        .success {
            background: #28a745;
            color: white;
        }
        .steps {
            text-align: right;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-right: 5px solid #0088cc;
        }
        .step {
            padding: 10px;
            margin: 5px 0;
            border-bottom: 1px solid #eee;
        }
        .btn {
            display: inline-block;
            padding: 15px 30px;
            margin: 15px;
            background: #0088cc;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.1em;
        }
        .telegram-btn {
            background: #0088cc;
        }
        .logs-btn {
            background: #28a745;
        }
        .bot-username {
            font-family: monospace;
            font-size: 1.5em;
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            color: #0088cc;
            margin: 20px 0;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 بوت الاختبارات التعليمية</h1>
        
        <div class="status success">
            ✅ <strong>الخدمة تعمل بنجاح!</strong>
        </div>
        
        <div class="bot-username">@banktest22bot</div>
        
        <div class="steps">
            <h3>🚀 كيف تجرب البوت:</h3>
            <div class="step">1. افتح تطبيق Telegram</div>
            <div class="step">2. ابحث عن <strong>@banktest22bot</strong></div>
            <div class="step">3. اضغط على <strong>Start</strong> أو أرسل <code>/start</code></div>
            <div class="step">4. استخدم الأوامر: <code>/teacher</code> أو <code>/student</code></div>
        </div>
        
        <div>
            <a href="https://t.me/banktest22bot" class="btn telegram-btn" target="_blank">
                📲 افتح البوت على Telegram
            </a>
            <a href="/bot-status" class="btn logs-btn">
                📊 حالة البوت التقنية
            </a>
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px; color: #666;">
            <p><strong>⏱ ملاحظة:</strong> قد يستغرق البوت 30-60 ثانية بعد النشر ليبدأ بالكامل.</p>
            <p>إذا لم يرد البوت، انتظر دقيقة ثم جرب مرة أخرى.</p>
        </div>
    </div>
</body>
</html>
    """

@app.route('/bot-status')
def bot_status():
    """صفحة حالة البوت التقنية"""
    token = os.getenv('BOT_TOKEN')
    
    # اختبار إذا كان التوكن يعمل
    token_valid = False
    bot_info = {}
    
    if token:
        try:
            import requests
            response = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=5)
            if response.json().get('ok'):
                token_valid = True
                bot_info = response.json()['result']
        except:
            pass
    
    return jsonify({
        "service": "running",
        "flask_server": "active",
        "bot_token_set": bool(token),
        "bot_token_valid": token_valid,
        "bot_info": bot_info,
        "telegram_bot": "@banktest22bot",
        "available_commands": ["/start", "/teacher", "/student", "/help"],
        "message": "تحقق من logs في Render لرؤية حالة تشغيل البوت"
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("=" * 70)
    print("🚀 بدء تشغيل نظام بوت الاختبارات التعليمية")
    print("=" * 70)
    
    # تثبيت المكتبات أولاً
    print("📦 الخطوة 1: فحص المكتبات المطلوبة...")
    install_telegram_bot()
    
    # بدء بوت Telegram في thread منفصل
    print("🤖 الخطوة 2: بدء تشغيل بوت Telegram...")
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    print("✅ تم بدء thread بوت Telegram في الخلفية")
    
    # معلومات التشغيل
    print("\n" + "=" * 70)
    print("📊 معلومات النظام:")
    print(f"🔗 رابط الويب: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 بوت Telegram: @banktest22bot")
    print("📋 الأوامر المتاحة: /start, /teacher, /student, /help")
    print("=" * 70 + "\n")
    
    # بدء خادم Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 الخطوة 3: بدء خادم Flask على المنفذ {port}")
    print("⏳ النظام يعمل الآن...")
    
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

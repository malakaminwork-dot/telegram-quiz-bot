from flask import Flask, jsonify
import os
import sys
import subprocess
import time
import threading

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
            # تثبيت المكتبات المطلوبة
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7", "requests==2.31.0"])
            print("✅ تم تثبيت المكتبات بنجاح")
            return True
        except Exception as e:
            print(f"❌ فشل تثبيت المكتبات: {e}")
            return False

# ========== تشغيل بوت Telegram ==========
def start_telegram_bot():
    """بدء تشغيل بوت Telegram بعد تثبيت المكتبات"""
    print("🤖 محاولة تشغيل بوت Telegram...")
    time.sleep(5)  # انتظار أكثر للتثبيت
    
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            print(f"🔧 المحاولة {attempt + 1} من {max_attempts}...")
            
            # استيراد المكتبات
            from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
            from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
            
            token = os.getenv('BOT_TOKEN')
            if not token:
                print("❌ BOT_TOKEN غير مضبوط")
                return
            
            print(f"✅ التوكن: {token[:15]}...")
            
            # اختبار التوكن مع API
            import requests
            try:
                test = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
                if test.json().get('ok'):
                    bot_info = test.json()['result']
                    print(f"✅ التوكن صحيح! البوت: @{bot_info['username']}")
                else:
                    print(f"❌ التوكن خاطئ: {test.json()}")
                    return
            except Exception as e:
                print(f"⚠️ خطأ في اختبار التوكن: {e}")
            
            # ========== دوال الرد ==========
            async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
                user = update.effective_user
                
                # إنشاء أزرار تفاعلية
                keyboard = [
                    [InlineKeyboardButton("👨‍🏫 أنا مدرس", callback_data='teacher_mode')],
                    [InlineKeyboardButton("👨‍🎓 أنا طالب", callback_data='student_mode')],
                    [InlineKeyboardButton("❓ المساعدة", callback_data='help_info')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"🎓 **مرحباً {user.first_name}!**\n\n"
                    "أهلاً بك في نظام الاختبارات التعليمية الذكي\n\n"
                    "اختر هويتك للبدء:",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            async def teacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
                user = update.effective_user
                
                keyboard = [
                    [InlineKeyboardButton("📝 إنشاء اختبار جديد", callback_data='create_quiz')],
                    [InlineKeyboardButton("📋 الاختبارات الحالية", callback_data='my_quizzes')],
                    [InlineKeyboardButton("📊 نتائج الطلاب", callback_data='student_results')],
                    [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='main_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"👨‍🏫 **مرحباً أستاذ {user.first_name}!**\n\n"
                    "**لوحة تحكم المدرس**\n\n"
                    "✨ المميزات المتاحة:\n"
                    "• إنشاء اختبارات جديدة\n"
                    "• إدارة الاختبارات الحالية\n"
                    "• متابعة نتائج الطلاب\n\n"
                    "اختر المهمة التي تريد تنفيذها:",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            async def student_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
                user = update.effective_user
                
                keyboard = [
                    [InlineKeyboardButton("📝 الاختبارات المتاحة", callback_data='available_quizzes')],
                    [InlineKeyboardButton("🏆 نتائجي", callback_data='my_results')],
                    [InlineKeyboardButton("🔍 بحث عن اختبار", callback_data='search_quiz')],
                    [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data='main_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"👨‍🎓 **مرحباً {user.first_name}!**\n\n"
                    "**لوحة الطالب**\n\n"
                    "✨ المميزات المتاحة:\n"
                    "• أداء الاختبارات المتاحة\n"
                    "• رؤية النتائج السابقة\n"
                    "• البحث عن اختبارات\n\n"
                    "ماذا تريد أن تفعل؟",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
                help_text = """
🆘 **مركز المساعدة - بوت الاختبارات التعليمية**

**👨‍🏫 للمدرسين:**
• /teacher - دخول وضع المدرس
• إنشاء اختبارات جديدة
• متابعة نتائج الطلاب
• إدارة الاختبارات الحالية

**👨‍🎓 للطلاب:**
• /student - دخول وضع الطالب
• أداء الاختبارات المتاحة
• رؤية النتائج السابقة
• البحث عن اختبارات

**📞 الأوامر الأساسية:**
• /start - بدء البوت والقائمة الرئيسية
• /help - عرض رسالة المساعدة هذه

**🚀 كيف تبدأ؟**
1. أرسل /start لرؤية القائمة الرئيسية
2. اختر "أنا مدرس" أو "أنا طالب"
3. ابدأ استخدام المميزات

✨ **البوت قيد التطوير، المزيد قريباً!**
                """
                await update.message.reply_text(help_text, parse_mode='Markdown')
            
            # معالجة أزرار callback
            async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
                query = update.callback_query
                await query.answer()
                
                if query.data == 'teacher_mode':
                    await query.edit_message_text(
                        "👨‍🏫 **تم تحديد وضع المدرس**\n\n"
                        "يمكنك الآن استخدام جميع مميزات المدرس:\n\n"
                        "• 📝 إنشاء اختبارات جديدة\n"
                        "• 📋 إدارة الاختبارات الحالية\n"
                        "• 📊 متابعة نتائج الطلاب\n\n"
                        "🚀 أرسل /teacher للبدء",
                        parse_mode='Markdown'
                    )
                elif query.data == 'student_mode':
                    await query.edit_message_text(
                        "👨‍🎓 **تم تحديد وضع الطالب**\n\n"
                        "يمكنك الآن استخدام جميع مميزات الطالب:\n\n"
                        "• 📝 أداء الاختبارات المتاحة\n"
                        "• 🏆 رؤية النتائج السابقة\n"
                        "• 🔍 البحث عن اختبارات\n\n"
                        "🚀 أرسل /student للبدء",
                        parse_mode='Markdown'
                    )
                elif query.data == 'help_info':
                    await help_command(query, context)
                elif query.data == 'main_menu':
                    await start_command(query, context)
                elif query.data == 'create_quiz':
                    await query.edit_message_text(
                        "📝 **إنشاء اختبار جديد**\n\n"
                        "هذه الميزة قيد التطوير حالياً.\n\n"
                        "قريباً ستتمكن من:\n"
                        "1. إدخال عنوان الاختبار\n"
                        "2. إضافة الأسئلة\n"
                        "3. تحديد الإجابات الصحيحة\n"
                        "4. إنشاء كود الاختبار\n\n"
                        "🚀 جاري العمل على هذه الميزة!",
                        parse_mode='Markdown'
                    )
                elif query.data == 'available_quizzes':
                    await query.edit_message_text(
                        "📝 **الاختبارات المتاحة**\n\n"
                        "هذه الميزة قيد التطوير حالياً.\n\n"
                        "قريباً ستتمكن من:\n"
                        "1. رؤية جميع الاختبارات المتاحة\n"
                        "2. البحث عن اختبارات\n"
                        "3. أداء الاختبارات مباشرة\n"
                        "4. رؤية النتائج فوراً\n\n"
                        "🚀 جاري العمل على هذه الميزة!",
                        parse_mode='Markdown'
                    )
            
            # ========== تشغيل البوت ==========
            print("🔧 جاري إنشاء تطبيق البوت...")
            application = Application.builder().token(token).build()
            
            # إضافة جميع handlers
            application.add_handler(CommandHandler("start", start_command))
            application.add_handler(CommandHandler("teacher", teacher_command))
            application.add_handler(CommandHandler("student", student_command))
            application.add_handler(CommandHandler("help", help_command))
            application.add_handler(CallbackQueryHandler(button_handler))
            
            print("✅ تم إضافة جميع الأوامر وال handlers!")
            print("📡 جاري بدء تشغيل البوت...")
            
            # تشغيل البوت بشكل صحيح - هذه هي السطر المهم!
            application.run_polling()
            
            print("🎉 بوت Telegram بدأ بنجاح!")
            return  # إذا وصل هنا، يعني نجح
            
        except ImportError as e:
            print(f"❌ مكتبة ناقصة في المحاولة {attempt + 1}: {e}")
            if attempt < max_attempts - 1:
                print("🔄 إعادة تثبيت المكتبات...")
                install_telegram_bot()
                time.sleep(10)
            else:
                print("❌ فشل جميع محاولات التثبيت")
                break
                
        except Exception as e:
            print(f"❌ خطأ في المحاولة {attempt + 1}: {type(e).__name__}: {e}")
            if attempt < max_attempts - 1:
                print(f"🔄 إعادة المحاولة بعد 10 ثواني...")
                time.sleep(10)
            else:
                print("❌ فشل تشغيل البوت بعد جميع المحاولات")
                break
    
    print("⚠️ بوت Telegram لم يبدأ بنجاح.")

# ========== صفحات الويب ==========
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 0;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            max-width: 800px;
            margin: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
            color: #333;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.8em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .status-box {
            padding: 25px;
            margin: 30px 0;
            border-radius: 15px;
            font-size: 1.3em;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7); }
            70% { box-shadow: 0 0 0 15px rgba(40, 167, 69, 0); }
            100% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
        }
        .success {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            border: none;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .feature-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border-top: 5px solid #0088cc;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-10px);
        }
        .feature-card h3 {
            color: #0088cc;
            margin-top: 0;
        }
        .commands {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            border-left: 5px solid #ffc107;
        }
        .command {
            display: inline-block;
            background: #e7f3ff;
            padding: 12px 25px;
            margin: 10px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #0088cc;
            border: 2px solid #b8d4ff;
        }
        .btn {
            display: inline-block;
            padding: 18px 40px;
            margin: 20px 15px;
            background: linear-gradient(135deg, #0088cc 0%, #0077b5 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: bold;
            font-size: 1.2em;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,136,204,0.3);
        }
        .btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,136,204,0.4);
        }
        .telegram-btn {
            background: linear-gradient(135deg, #0088cc 0%, #0077b5 100%);
        }
        .status-btn {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }
        .bot-info {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            margin: 25px 0;
            text-align: center;
        }
        .bot-username {
            font-family: 'Courier New', monospace;
            font-size: 1.8em;
            color: #0088cc;
            font-weight: bold;
            background: #e7f3ff;
            padding: 15px;
            border-radius: 10px;
            display: inline-block;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 بوت الاختبارات التعليمية</h1>
        <p style="color: #666; font-size: 1.2em; margin-bottom: 30px;">
            نظام متكامل لإدارة وتنفيذ الاختبارات التعليمية على Telegram
        </p>
        
        <div class="status-box success">
            ✅ <strong>النظام يعمل بنجاح!</strong>
            <div style="margin-top: 10px; font-size: 0.9em;">
                البوت نشط وجاهز للاستخدام
            </div>
        </div>
        
        <div class="bot-info">
            <h3 style="color: #2c3e50; margin-bottom: 15px;">🔗 رابط البوت على Telegram:</h3>
            <div class="bot-username">@banktest22bot</div>
            <p style="color: #666; margin-top: 10px;">
                اضغط على الاسم لفتح البوت مباشرة
            </p>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <h3>👨‍🏫 للمدرسين</h3>
                <p>• إنشاء اختبارات جديدة</p>
                <p>• إدارة الاختبارات الحالية</p>
                <p>• متابعة نتائج الطلاب</p>
                <p>• تحليل الأداء</p>
            </div>
            
            <div class="feature-card">
                <h3>👨‍🎓 للطلاب</h3>
                <p>• أداء الاختبارات المتاحة</p>
                <p>• رؤية النتائج فوراً</p>
                <p>• متابعة التقدم</p>
                <p>• شهادات الإنجاز</p>
            </div>
            
            <div class="feature-card">
                <h3>✨ المميزات</h3>
                <p>• واجهة سهلة الاستخدام</p>
                <p>• نتائج فورية</p>
                <p>• إحصائيات مفصلة</p>
                <p>• دعم الصور في الأسئلة</p>
            </div>
        </div>
        
        <div class="commands">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">📋 الأوامر المتاحة:</h3>
            <div class="command">/start</div>
            <div class="command">/teacher</div>
            <div class="command">/student</div>
            <div class="command">/help</div>
        </div>
        
        <div>
            <a href="https://t.me/banktest22bot" class="btn telegram-btn" target="_blank">
                📲 افتح البوت على Telegram
            </a>
            <a href="/system-status" class="btn status-btn">
                📊 حالة النظام التقنية
            </a>
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 12px; color: #666;">
            <p><strong>💡 معلومة:</strong> قد يستغرق البوت 30-60 ثانية بعد النشر ليصبح جاهزاً تماماً.</p>
            <p>إذا لم يرد البوت فوراً، انتظر دقيقة وجرب مرة أخرى.</p>
        </div>
        
        <div style="margin-top: 30px; font-size: 0.9em; color: #888;">
            <p>🚀 تم التطوير بواسطة Malak | نظام الاختبارات التعليمية © 2026</p>
        </div>
    </div>
</body>
</html>
    """

@app.route('/system-status')
def system_status():
    """صفحة الحالة التقنية للنظام"""
    try:
        import telegram
        lib_status = "✅ مثبتة وجاهزة"
    except ImportError:
        lib_status = "❌ غير مثبتة"
    
    token = os.getenv('BOT_TOKEN')
    
    return jsonify({
        "system": "Telegram Quiz Bot",
        "status": "running",
        "web_server": "Flask",
        "bot_library": lib_status,
        "bot_token_configured": "✅ نعم" if token else "❌ لا",
        "bot_username": "@banktest22bot",
        "available_commands": ["/start", "/teacher", "/student", "/help"],
        "web_url": "https://quiz-bot-final-q6sq.onrender.com",
        "telegram_bot_url": "https://t.me/banktest22bot",
        "message": "النظام يعمل بنجاح! جرب الأوامر على Telegram."
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 بدء تشغيل نظام بوت الاختبارات التعليمية")
    print("=" * 60)
    
    # تثبيت المكتبات أولاً
    print("📦 جاري فحص وتثبيت المكتبات المطلوبة...")
    install_telegram_bot()
    
    # بدء بوت Telegram في thread منفصل
    print("🤖 جاري بدء تشغيل بوت Telegram في الخلفية...")
    bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    bot_thread.start()
    print("✅ بدأ thread بوت Telegram")
    
    # معلومات التشغيل
    print("\n" + "=" * 60)
    print("📊 معلومات التشغيل:")
    print(f"🔗 رابط الويب: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 بوت Telegram: @banktest22bot")
    print("📋 الأوامر المتاحة: /start, /teacher, /student, /help")
    print("=" * 60 + "\n")
    
    # بدء خادم Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 بدء خادم الويب Flask على المنفذ {port}")
    print("⏳ جاري تشغيل النظام...")
    
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

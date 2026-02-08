from flask import Flask, jsonify
import os
import sys
import threading
import asyncio

app = Flask(__name__)

# ========== تشغيل بوت Telegram ==========
async def run_telegram_bot_async():
    """تشغيل البوت باستخدام asyncio"""
    try:
        print("🤖 جاري تحميل مكتبات Telegram...")
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ BOT_TOKEN غير مضبوط")
            return
        
        print(f"✅ التوكن: {token[:10]}...")
        
        # ========== جميع دوال الرد ==========
        
        # أمر /start
        async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            
            # إنشاء أزرار
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
        
        # أمر /teacher
        async def teacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            
            keyboard = [
                [InlineKeyboardButton("📝 إنشاء اختبار جديد", callback_data='create_quiz')],
                [InlineKeyboardButton("📋 الاختبارات الحالية", callback_data='my_quizzes')],
                [InlineKeyboardButton("📊 نتائج الطلاب", callback_data='student_results')],
                [InlineKeyboardButton("🔙 رجوع", callback_data='back_to_start')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"👨‍🏫 **مرحباً أستاذ {user.first_name}!**\n\n"
                "**لوحة تحكم المدرس**\n\n"
                "اختر المهمة التي تريد تنفيذها:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        # أمر /student
        async def student_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            
            keyboard = [
                [InlineKeyboardButton("📝 الاختبارات المتاحة", callback_data='available_quizzes')],
                [InlineKeyboardButton("🏆 نتائجي", callback_data='my_results')],
                [InlineKeyboardButton("🔍 بحث عن اختبار", callback_data='search_quiz')],
                [InlineKeyboardButton("🔙 رجوع", callback_data='back_to_start')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"👨‍🎓 **مرحباً {user.first_name}!**\n\n"
                "**لوحة الطالب**\n\n"
                "ماذا تريد أن تفعل؟",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        # أمر /help
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            help_text = """
🆘 **مركز المساعدة**

**👨‍🏫 للمدرسين:**
• /teacher - دخول وضع المدرس
• إنشاء اختبارات جديدة
• متابعة نتائج الطلاب

**👨‍🎓 للطلاب:**
• /student - دخول وضع الطالب
• أداء الاختبارات المتاحة
• رؤية النتائج السابقة

**📞 للأوامر:**
• /start - بدء البوت
• /help - هذه الرسالة

🚀 **ابدأ الآن بإرسال /teacher أو /student**
            """
            await update.message.reply_text(help_text, parse_mode='Markdown')
        
        # معالجة أزرار callback
        async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            await query.answer()
            
            if query.data == 'teacher_mode':
                await query.edit_message_text(
                    "👨‍🏫 **تم تحديد وضع المدرس**\n\n"
                    "يمكنك الآن:\n"
                    "• إنشاء اختبارات جديدة\n"
                    "• إدارة اختباراتك\n"
                    "• رؤية نتائج الطلاب\n\n"
                    "🚀 أرسل /teacher للبدء"
                )
            elif query.data == 'student_mode':
                await query.edit_message_text(
                    "👨‍🎓 **تم تحديد وضع الطالب**\n\n"
                    "يمكنك الآن:\n"
                    "• رؤية الاختبارات المتاحة\n"
                    "• أداء الاختبارات\n"
                    "• رؤية نتائجك\n\n"
                    "🚀 أرسل /student للبدء"
                )
            elif query.data == 'help_info':
                await query.edit_message_text(
                    "❓ **المساعدة السريعة**\n\n"
                    "1. للمدرسين: أرسل /teacher\n"
                    "2. للطلاب: أرسل /student\n"
                    "3. للمساعدة التفصيلية: /help\n\n"
                    "🎯 جرب الآن!"
                )
            elif query.data == 'back_to_start':
                await start_command(query, context)
        
        # ========== إنشاء وتشغيل البوت ==========
        print("🔧 جاري إنشاء تطبيق البوت...")
        application = Application.builder().token(token).build()
        
        # إضافة جميع handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("teacher", teacher_command))
        application.add_handler(CommandHandler("student", student_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        print("✅ جميع الأوامر مضافَة!")
        print("📋 الأوامر المتاحة: /start, /teacher, /student, /help")
        
        # بدء البوت
        print("🚀 بدء تشغيل البوت...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        print("🎉 بوت Telegram يعمل بنجاح!")
        print("👉 جرب الأوامر: /teacher أو /student")
        
        # إبقاء البوت يعمل
        await asyncio.Event().wait()
        
    except ImportError as e:
        print(f"❌ مكتبة ناقصة: {e}")
        print("📦 قم بتثبيت: pip install python-telegram-bot")
    except Exception as e:
        print(f"❌ خطأ في البوت: {e}")

def run_telegram_bot():
    """تشغيل البوت في loop منفصل"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_telegram_bot_async())
    except Exception as e:
        print(f"❌ فشل تشغيل البوت: {e}")
    finally:
        loop.close()

# ========== صفحات الويب ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><title>بوت الاختبارات</title>
<style>
body{font-family:Arial; padding:50px; text-align:center; background:linear-gradient(135deg,#667eea,#764ba2); color:white;}
.container{max-width:700px; margin:0 auto; background:rgba(255,255,255,0.95); padding:40px; border-radius:20px; color:#333; box-shadow:0 20px 40px rgba(0,0,0,0.2);}
h1{color:#2c3e50;}
.card{background:#f8f9fa; padding:20px; margin:20px 0; border-radius:10px; border-right:5px solid #28a745;}
.command{background:#e7f3ff; padding:10px; margin:5px; border-radius:5px; display:inline-block;}
.btn{padding:12px 25px; margin:10px; background:#28a745; color:white; text-decoration:none; border-radius:8px; font-weight:bold; display:inline-block;}
.telegram{background:#0088cc;}
</style></head>
<body>
<div class="container">
    <h1>🤖 بوت الاختبارات التعليمية</h1>
    
    <div class="card">
        <h2>✅ البوت يعمل بنجاح!</h2>
        <p><strong>البوت:</strong> @banktest22bot</p>
        <p><strong>الحالة:</strong> نشط وجاهز</p>
    </div>
    
    <div class="card">
        <h3>📋 الأوامر المتاحة:</h3>
        <div class="command"><code>/start</code> - بدء البوت</div>
        <div class="command"><code>/teacher</code> - وضع المدرس</div>
        <div class="command"><code>/student</code> - وضع الطالب</div>
        <div class="command"><code>/help</code> - المساعدة</div>
    </div>
    
    <div class="card">
        <h3>🚀 جرب الآن على Telegram:</h3>
        <p>1. افتح @banktest22bot</p>
        <p>2. أرسل <code>/teacher</code> أو <code>/student</code></p>
        <p>3. شاهد القائمة التفاعلية</p>
    </div>
    
    <div>
        <a href="https://t.me/banktest22bot" class="btn telegram" target="_blank">
            📲 افتح البوت الآن
        </a>
        <a href="/status" class="btn">
            📊 حالة النظام
        </a>
    </div>
</div>
</body>
</html>
    """

@app.route('/status')
def status():
    token = os.getenv('BOT_TOKEN')
    return jsonify({
        "status": "running",
        "bot": "@banktest22bot",
        "commands": ["/start", "/teacher", "/student", "/help"],
        "message": "جرب الأوامر على Telegram!"
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("🚀 بدء تشغيل نظام البوت...")
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 البوت: @banktest22bot")
    print("📋 الأوامر: /start, /teacher, /student, /help")
    
    # بدء بوت Telegram في thread منفصل
    try:
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()
        print("✅ بدأ بوت Telegram في الخلفية")
    except Exception as e:
        print(f"⚠️ لم يبدأ البوت: {e}")
    
    # بدء خادم Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 خادم الويب على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

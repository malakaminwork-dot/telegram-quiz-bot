from flask import Flask, jsonify
import os
import sys
import subprocess
import time

app = Flask(__name__)

# ========== تثبيت المكتبات المطلوبة ==========
def install_requirements():
    print("📦 تثبيت المكتبات المطلوبة...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7", "Flask==2.3.2", "requests==2.31.0"])
        print("✅ تم تثبيت المكتبات")
        return True
    except:
        print("❌ فشل التثبيت")
        return False

# ========== تشغيل البوت بشكل منفصل ==========
def run_bot_separately():
    """تشغيل البوت في عملية منفصلة"""
    print("🤖 جاري تشغيل البوت في عملية منفصلة...")
    
    # الكود الذي سيتم تنفيذه في العملية المنفصلة
    bot_code = '''
import os
import sys
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 **أهلاً! البوت يعمل الآن!**")

async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👨‍🏫 **وضع المدرس - جاهز!**")

async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👨‍🎓 **وضع الطالب - جاهز!**")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆘 **/start, /teacher, /student, /help**")

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN غير مضبوط")
        return
    
    print(f"✅ التوكن: {token[:15]}...")
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("teacher", teacher))
    app.add_handler(CommandHandler("student", student))
    app.add_handler(CommandHandler("help", help_cmd))
    
    print("✅ البوت جاهز! جاري التشغيل...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    print("🎉 البوت يعمل ويستمع للرسائل!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    # حفظ الكود في ملف منفصل وتشغيله
    with open('bot_runner.py', 'w', encoding='utf-8') as f:
        f.write(bot_code)
    
    # تشغيل البوت في عملية منفصلة
    try:
        subprocess.Popen([sys.executable, 'bot_runner.py'])
        print("✅ بدأ تشغيل البوت في عملية منفصلة")
        return True
    except:
        print("❌ فشل تشغيل البوت")
        return False

# ========== صفحات الويب ==========
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><title>بوت الاختبارات</title>
<style>
body{font-family:Arial; padding:40px; text-align:center; background:#f0f8ff;}
.container{max-width:600px; margin:0 auto; background:white; padding:30px; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);}
h1{color:#2c3e50;}
.success{background:#28a745; color:white; padding:15px; border-radius:8px; margin:20px 0;}
.btn{display:inline-block; padding:12px 25px; margin:10px; background:#0088cc; color:white; text-decoration:none; border-radius:8px; font-weight:bold;}
</style></head>
<body>
<div class="container">
    <h1>🤖 بوت الاختبارات التعليمية</h1>
    <div class="success">✅ النظام يعمل بنجاح!</div>
    <p>البوت: <strong>@banktest22bot</strong></p>
    <p>جرب الأوامر على Telegram:</p>
    <p><code>/start</code> <code>/teacher</code> <code>/student</code> <code>/help</code></p>
    <a href="https://t.me/banktest22bot" class="btn" target="_blank">📲 افتح البوت</a>
</div>
</body>
</html>
"""

@app.route('/status')
def status():
    return jsonify({
        "status": "running",
        "bot": "@banktest22bot",
        "service": "quiz-bot-final-q6sq.onrender.com"
    })

# ========== بدء التشغيل ==========
if __name__ == '__main__':
    print("🚀 بدء تشغيل الخدمة...")
    
    # تثبيت المكتبات
    install_requirements()
    
    # بدء البوت في عملية منفصلة
    run_bot_separately()
    
    # بدء Flask
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 خادم الويب على المنفذ {port}")
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 البوت: @banktest22bot")
    print("📋 الأوامر: /start, /teacher, /student, /help")
    
    app.run(host='0.0.0.0', port=port, debug=False)

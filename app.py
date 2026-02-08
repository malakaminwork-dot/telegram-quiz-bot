from flask import Flask, jsonify
import os
import threading
import time
import asyncio
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
    <title>بوت الاختبارات - التشغيل الآن ✅</title>
    <style>
        body { font-family: Arial; padding: 40px; text-align: center; background: #f0f8ff; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .status { padding: 20px; margin: 20px 0; border-radius: 10px; font-size: 1.2em; }
        .green { background: #d4edda; color: #155724; border: 2px solid #c3e6cb; }
        .blue { background: #d1ecf1; color: #0c5460; border: 2px solid #bee5eb; }
        .btn { display: inline-block; padding: 12px 30px; margin: 15px; background: #28a745; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }
        .telegram { background: #0088cc; }
        code { background: #f8f9fa; padding: 3px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 بوت الاختبارات - الإصدار النهائي</h1>
        
        <div class="status green">
            ✅ <strong>الخدمة تعمل - جاري تشغيل البوت...</strong>
        </div>
        
        <div class="status blue">
            <p>📋 <strong>التشخيص:</strong> تم إصلاح خطأ التشغيل</p>
            <p>🤖 <strong>البوت:</strong> @banktest22bot</p>
            <p>🔗 <strong>الرابط:</strong> quiz-bot-final-q6sq.onrender.com</p>
        </div>
        
        <h3>🚀 جرب الآن:</h3>
        <ol style="text-align: right; margin: 20px auto; width: 300px;">
            <li>افتح Telegram</li>
            <li>ابحث عن <code>@banktest22bot</code></li>
            <li>اضغط <strong>Start</strong></li>
            <li>أرسل <code>/start</code></li>
        </ol>
        
        <div>
            <a href="https://t.me/banktest22bot" class="btn telegram" target="_blank">
                📲 افتح البوت على Telegram
            </a>
            <a href="/test" class="btn">
                🔍 اختبر البوت
            </a>
        </div>
        
        <p style="margin-top: 30px; color: #666; font-size: 0.9em;">
            ⏱ قد يستغرق البوت 30 ثانية بعد النشر ليصبح جاهزاً.
        </p>
    </div>
</body>
</html>
    """

@app.route('/test')
def test():
    """صفحة اختبار بسيطة"""
    token = os.getenv('BOT_TOKEN')
    return jsonify({
        "status": "running",
        "bot_token": "✅ مضبوط" if token else "❌ غير مضبوط",
        "bot_username": "@banktest22bot",
        "message": "البوت يعمل الآن! جرب /start"
    })

# ========== تشغيل بوت Telegram بشكل صحيح ==========
async def run_bot_async():
    """تشغيل البوت باستخدام asyncio"""
    try:
        print("🔧 جاري استيراد مكتبات بوت Telegram...")
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            print("❌ BOT_TOKEN غير مضبوط")
            return
        
        print(f"✅ التوكن: {token[:10]}...")
        
        # دالة الرد على /start
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🎊 **أهلاً وسهلاً!**\n\n"
                "✅ بوت الاختبارات التعليمية يعمل بنجاح!\n\n"
                "✨ يمكنك الآن:\n"
                "• إنشاء الاختبارات\n• إجراء الاختبارات\n• عرض النتائج\n\n"
                "🚀 ابدأ رحلتك التعليمية!"
            )
        
        # إنشاء التطبيق
        print("🤖 جاري إنشاء تطبيق البوت...")
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", start))
        
        print("✅ البوت جاهز! جاري التشغيل...")
        print("📞 أرسل /start إلى @banktest22bot")
        
        # تشغيل البوت (هذه المرة بشكل صحيح)
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # إبقاء البوت يعمل
        print("🎯 بوت Telegram يعمل الآن بنجاح!")
        await asyncio.Event().wait()  # يبقى البوت يعمل للأبد
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

def run_bot():
    """تشغيل البوت في loop منفصل"""
    print("🚀 بدء تشغيل بوت Telegram...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot_async())
    except Exception as e:
        print(f"❌ فشل تشغيل البوت: {e}")
    finally:
        loop.close()

# بدء البوت عند تشغيل التطبيق
if os.getenv('BOT_TOKEN'):
    print("🔑 تم العثور على BOT_TOKEN، جاري بدء البوت...")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("✅ بدأ thread البوت في الخلفية")
else:
    print("⚠️ BOT_TOKEN غير مضبوط، البوت لن يعمل")

# ========== بدء خادم Flask ==========
if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    print(f"🌐 بدء خادم الويب على المنفذ {port}")
    print(f"🔗 الرابط: https://quiz-bot-final-q6sq.onrender.com")
    print(f"🤖 البوت: @banktest22bot")
    print("⏳ يرجى الانتظار 30 ثانية حتى يبدأ البوت...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

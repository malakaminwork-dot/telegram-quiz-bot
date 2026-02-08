from flask import Flask, jsonify
import os
import threading
import logging

app = Flask(__name__)

# ========== الصفحات الأساسية ==========
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>بوت الاختبارات</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f2f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        .status { padding: 15px; margin: 20px 0; border-radius: 8px; font-weight: bold; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .bot-link { display: inline-block; background: #25D366; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; margin: 15px; font-size: 18px; }
        .telegram-btn { background: #0088cc; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; margin: 10px; display: inline-block; }
        code { background: #f8f9fa; padding: 5px 10px; border-radius: 4px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 بوت الاختبارات التعليمية</h1>
        
        <div class="status success">
            ✅ <strong>الخدمة تعمل بنجاح!</strong>
        </div>
        
        <div class="status info">
            <p>🔗 رابط الخدمة: <code>quiz-bot-final-q6sq.onrender.com</code></p>
            <p>🤖 بوت Telegram: <strong>@banktest22bot</strong></p>
        </div>
        
        <h3>🚀 خطوات التشغيل:</h3>
        <ol style="text-align: right; margin: 20px auto; width: 300px;">
            <li>افتح Telegram</li>
            <li>ابحث عن <strong>@banktest22bot</strong></li>
            <li>أرسل <code>/start</code></li>
            <li>استلم رسالة الترحيب!</li>
        </ol>
        
        <div>
            <a href="https://t.me/banktest22bot" class="telegram-btn" target="_blank">
                📲 افتح البوت على Telegram
            </a>
            <a href="/bot-status" class="bot-link">
                📊 حالة البوت
            </a>
        </div>
        
        <p style="margin-top: 30px; color: #666;">
            إذا لم يعمل البوت، تحقق من <code>BOT_TOKEN</code> في إعدادات Render
        </p>
    </div>
</body>
</html>
    """

@app.route('/bot-status')
def bot_status():
    token = os.getenv('BOT_TOKEN')
    return jsonify({
        "service": "running",
        "bot_token_set": "✅ نعم" if token else "❌ لا",
        "next_step": "تحقق من BOT_TOKEN في Render" if not token else "البوت جاهز"
    })

# ========== بدء البوت بعد التأكد من المكتبات ==========
def start_bot_after_import():
    """بدء البوت بعد استيراد المكتبات المطلوبة"""
    try:
        # حاول استيراد المكتبات أولاً
        import requests
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        
        token = os.getenv('BOT_TOKEN')
        if not token:
            logging.error("BOT_TOKEN غير مضبوط")
            return
        
        # اختبار التوكن
        test = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=5)
        if test.json().get('ok'):
            print(f"✅ التوكن صحيح! البوت: {test.json()['result']['username']}")
            
            # تشغيل البوت
            async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                await update.message.reply_text('🎉 البوت يعمل! مرحباً!')
            
            app = Application.builder().token(token).build()
            app.add_handler(CommandHandler("start", start))
            print("🤖 بدء استماع البوت للرسائل...")
            app.run_polling()
            
    except ImportError as e:
        print(f"❌ مكتبة ناقصة: {e}. أضفها إلى requirements.txt")
    except Exception as e:
        print(f"❌ خطأ: {e}")

# بدء البوت في الخلفية
if __name__ == '__main__':
    # حاول تشغيل البوت في thread منفصل
    try:
        bot_thread = threading.Thread(target=start_bot_after_import, daemon=True)
        bot_thread.start()
        print("🚀 بدء محاولة تشغيل البوت...")
    except:
        print("⚠️ لم يبدأ البوت بعد. تحقق من المكتبات.")
    
    # تشغيل Flask
    port = int(os.getenv('PORT', 10000))
    print(f"🌐 بدء خادم الويب على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

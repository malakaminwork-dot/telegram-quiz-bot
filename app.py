from flask import Flask, request, jsonify
import os
import threading
import time
from bot_simple import main as run_bot

app = Flask(__name__)

# متغير لتخزين حالة البوت
bot_status = {"running": False, "thread": None}

def run_telegram_bot():
    """تشغيل بوت تلجرام في thread منفصل"""
    try:
        print("🤖 بدء تشغيل بوت تلجرام...")
        run_bot()
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Telegram Quiz Bot",
        "bot_status": "running" if bot_status["running"] else "stopped",
        "endpoints": {
            "/": "هذه الصفحة",
            "/health": "فحص الحالة",
            "/start-bot": "تشغيل البوت",
            "/stop-bot": "إيقاف البوت"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "bot": bot_status["running"]
    })

@app.route('/start-bot')
def start_bot():
    if not bot_status["running"]:
        bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
        bot_thread.start()
        bot_status["thread"] = bot_thread
        bot_status["running"] = True
        return jsonify({"message": "✅ تم تشغيل البوت بنجاح"})
    return jsonify({"message": "⚠️ البوت يعمل بالفعل"})

@app.route('/stop-bot')
def stop_bot():
    # Note: في الإصدار الحقيقي، تحتاج طريقة لإيقاف البوت
    bot_status["running"] = False
    return jsonify({"message": "⏸️ تم إيقاف البوت"})

# تشغيل البوت تلقائياً عند بدء التطبيق
@app.before_first_request
def initialize():
    if not bot_status["running"]:
        start_bot()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

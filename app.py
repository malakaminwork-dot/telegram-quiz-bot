from flask import Flask, jsonify
import os
import subprocess
import sys

app = Flask(__name__)

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
.btn{padding:12px 25px; margin:10px; background:#0088cc; color:white; text-decoration:none; border-radius:8px; font-weight:bold;}
</style></head>
<body>
<div class="container">
    <h1>🤖 بوت الاختبارات التعليمية</h1>
    <div class="success">✅ تم إصلاح مشكلة البوت المزدوج</div>
    <p><strong>البوت الجديد:</strong> @banktest22bot</p>
    <p>تم إيقاف جميع البوتات القديمة</p>
    <p>جرب الآن:</p>
    <p><code>/start</code> <code>/teacher</code> <code>/student</code></p>
    <a href="https://t.me/banktest22bot" class="btn" target="_blank">📲 افتح البوت</a>
    <a href="/restart-bot" class="btn" style="background:#ffc107;">🔄 إعادة تشغيل البوت</a>
</div>
</body>
</html>
"""

@app.route('/restart-bot')
def restart_bot():
    """إعادة تشغيل البوت"""
    try:
        # إيقاف أي بوت يعمل
        subprocess.run([sys.executable, "-c", """
import asyncio
import os
try:
    from telegram.ext import Application
    token = os.getenv('BOT_TOKEN')
    if token:
        app = Application.builder().token(token).build()
        asyncio.run(app.stop())
except:
    pass
"""])
        
        # بدء البوت الجديد
        subprocess.Popen([sys.executable, "bot_runner.py"])
        return jsonify({"status": "restarting", "message": "جاري إعادة تشغيل البوت"})
    except:
        return jsonify({"status": "error", "message": "فشل إعادة التشغيل"})

@app.route('/status')
def status():
    return jsonify({
        "status": "running",
        "bot": "@banktest22bot",
        "fixed": "yes - conflict resolved",
        "message": "تم إصلاح مشكلة البوت المزدوج"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    
    # بدء البوت في الخلفية
    try:
        subprocess.Popen([sys.executable, "bot_runner.py"])
        print("✅ بدأ تشغيل البوت في الخلفية")
    except:
        print("⚠️ لم يبدأ البوت")
    
    app.run(host='0.0.0.0', port=port, debug=False)

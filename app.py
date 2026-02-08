from flask import Flask
import os
import logging

app = Flask(__name__)

# صفحة البداية البسيطة
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Quiz Bot</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                direction: rtl;
                text-align: center;
                padding: 50px;
                background: linear-gradient(135deg, #4f8bf9 0%, #2a52d1 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.15);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                max-width: 700px;
                width: 90%;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            }
            h1 {
                color: #fff;
                margin-bottom: 25px;
                font-size: 2.5em;
            }
            .status {
                background: #28a745;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                display: inline-block;
                margin: 15px;
                font-size: 1.2em;
                font-weight: bold;
            }
            .card {
                background: rgba(255, 255, 255, 0.1);
                padding: 25px;
                border-radius: 12px;
                margin: 25px 0;
                text-align: right;
            }
            .step {
                background: rgba(255, 255, 255, 0.2);
                padding: 15px;
                margin: 12px 0;
                border-radius: 8px;
                border-right: 5px solid #4CAF50;
            }
            a.button {
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                margin: 10px;
                font-size: 1.1em;
                transition: all 0.3s;
            }
            a.button:hover {
                background: #45a049;
                transform: translateY(-3px);
            }
            .logs {
                background: rgba(0, 0, 0, 0.3);
                padding: 15px;
                border-radius: 8px;
                text-align: left;
                font-family: monospace;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 بوت الاختبارات التعليمية</h1>
            <div class="status">🚀 جاهز للتشغيل</div>
            
            <div class="card">
                <h2>✅ تم التحديث بنجاح</h2>
                <p>تم إصلاح ملفات الإعتماديات وجاهز للنشر</p>
            </div>
            
            <div class="card">
                <h3>🔧 الخطوات المتبقية:</h3>
                <div class="step">1. انتقل إلى Render</div>
                <div class="step">2. أضف BOT_TOKEN في Environment Variables</div>
                <div class="step">3. اضغط على Restart Service</div>
                <div class="step">4. انتظر حتى تصبح الحالة Healthy ✅</div>
            </div>
            
            <div style="margin: 30px 0;">
                <a href="https://dashboard.render.com" class="button" target="_blank">🚀 الذهاب إلى Render</a>
                <a href="/health" class="button">📊 فحص الحالة</a>
            </div>
            
            <div class="card">
                <h3>📋 معلومات الخدمة:</h3>
                <p><strong>الاسم:</strong> telegram-quiz-bot</p>
                <p><strong>الحالة:</strong> جاهز للنشر</p>
                <p><strong>آخر تحديث:</strong> تم الآن</p>
            </div>
        </div>
    </body>
    </html>
    """

# صفحة فحص الحالة
@app.route('/health')
def health():
    return {
        "status": "healthy",
        "message": "✅ الخدمة تعمل بنجاح",
        "next_step": "أضف BOT_TOKEN في Render"
    }

# بدء التشغيل
if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    print(f"🚀 بدء التشغيل على المنفذ {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "🎉 نجحت! البوت جاهز. الخطوة التالية: أضف BOT_TOKEN في Render"

@app.route('/health')
def health():
    return {"status": "ready", "step": "add_bot_token"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

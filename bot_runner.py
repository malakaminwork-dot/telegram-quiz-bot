import os
import asyncio
import sys

# إضافة المسار الحالي للبحث عن المكتبات
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    print("🤖 بدء تشغيل بوت Telegram...")
    
    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        
        token = os.getenv("BOT_TOKEN")
        if not token:
            print("❌ خطأ: BOT_TOKEN غير مضبوط!")
            return
        
        print(f"✅ التوكن: {token[:15]}...")
        
        # اختبار التوكن
        import requests
        try:
            test = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=10)
            if test.json().get('ok'):
                bot_info = test.json()['result']
                print(f"✅ البوت: @{bot_info['username']}")
            else:
                print(f"❌ التوكن غير صالح: {test.json()}")
                return
        except Exception as e:
            print(f"⚠️ خطأ في اختبار التوكن: {e}")
        
        # دوال الرد
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🎉 **مرحباً! البوت يعمل الآن!**\n\n"
                "✨ الأوامر المتاحة:\n"
                "• /teacher - وضع المدرس\n"
                "• /student - وضع الطالب\n"
                "• /help - المساعدة\n\n"
                "🚀 جرب الآن!"
            )
        
        async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🏫 **وضع المدرس**\n\n"
                "مميزات قريباً:\n"
                "• إنشاء اختبارات\n"
                "• إدارة الاختبارات\n"
                "• نتائج الطلاب\n\n"
                "🚀 قيد التطوير!"
            )
        
        async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "👨‍🎓 **وضع الطالب**\n\n"
                "مميزات قريباً:\n"
                "• أداء الاختبارات\n"
                "• رؤية النتائج\n"
                "• متابعة التقدم\n\n"
                "🚀 قيد التطوير!"
            )
        
        async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(
                "🆘 **مساعدة**\n\n"
                "الأوامر:\n"
                "• /start - بدء البوت\n"
                "• /teacher - وضع المدرس\n"
                "• /student - وضع الطالب\n"
                "• /help - هذه الرسالة\n\n"
                "🎯 جرب الآن!"
            )
        
        # إنشاء وتشغيل البوت
        app = Application.builder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("teacher", teacher))
        app.add_handler(CommandHandler("student", student))
        app.add_handler(CommandHandler("help", help_cmd))
        
        print("✅ البوت جاهز! جاري التشغيل...")
        
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        print("🎉 البوت يعمل ويستمع للرسائل الآن!")
        print("📞 أرسل /start إلى @banktest22bot")
        
        # إبقاء البوت يعمل
        await asyncio.Event().wait()
        
    except ImportError as e:
        print(f"❌ مكتبة ناقصة: {e}")
        print("📦 قم بتثبيت: pip install python-telegram-bot")
    except Exception as e:
        print(f"❌ خطأ: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio
import sys

import os
import asyncio
import sys
import time

# تأكد من أن هذا هو البوت الوحيد الذي يعمل
print("🔄 جاري إيقاف أي بوتات أخرى تعمل بنفس التوكن...")

# إضافة المسار الحالي للبحث عن المكتبات
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def stop_other_bots():
    """إيقاف أي عمليات بوت أخرى"""
    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
        
        token = os.getenv("BOT_TOKEN")
        if not token:
            return
        
        # إنشاء تطبيق مؤقت لإغلاق الاتصال السابق
        temp_app = Application.builder().token(token).build()
        
        try:
            await temp_app.initialize()
            await temp_app.start()
            
            # إغلاق أي اتصالات سابقة
            await temp_app.updater.stop()
            await temp_app.stop()
            await temp_app.shutdown()
            
            print("✅ تم إغلاق الاتصالات السابقة")
        except:
            print("⚠️ لا توجد اتصالات سابقة نشطة")
        finally:
            await asyncio.sleep(2)  # انتظار لضمان الإغلاق
            
    except ImportError:
        print("📦 المكتبات غير مثبتة بعد")
    except Exception as e:
        print(f"⚠️ خطأ في الإيقاف: {e}")

async def main():
    print("=" * 50)
    print("🤖 بدء تشغيل بوت Telegram الجديد")
    print("=" * 50)
    
    # انتظار للتأكد من إيقاف البوتات الأخرى
    await asyncio.sleep(3)
    
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
                print(f"📛 الاسم: {bot_info['first_name']}")
            else:
                print(f"❌ التوكن غير صالح: {test.json()}")
                return
        except Exception as e:
            print(f"⚠️ خطأ في اختبار التوكن: {e}")
        
        # دوال الرد البسيطة
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🎉 **أهلاً! هذا هو البوت الجديد!**")
        
        async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("👨‍🏫 **وضع المدرس - جاهز**")
        
        async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("👨‍🎓 **وضع الطالب - جاهز**")
        
        async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🆘 **/start, /teacher, /student, /help**")
        
        # إنشاء التطبيق مع إعدادات خاصة
        app = Application.builder().token(token).build()
        
        # إضافة handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("teacher", teacher))
        app.add_handler(CommandHandler("student", student))
        app.add_handler(CommandHandler("help", help_cmd))
        
        print("✅ البوت جاهز! جاري التشغيل...")
        
        # إعداد polling مع إعدادات خاصة
        await app.initialize()
        await app.start()
        
        # استخدم offset -1 للتأكد من البدء من الصفر
        await app.updater.start_polling(
            poll_interval=1.0,
            timeout=10,
            drop_pending_updates=True,  # تجاهل الرسائل القديمة
            allowed_updates=['message', 'callback_query']
        )
        
        print("=" * 50)
        print("🎉 **البوت يعمل الآن بنجاح!**")
        print("📞 أرسل /start إلى @banktest22bot")
        print("=" * 50)
        
        # إبقاء البوت يعمل
        await asyncio.Event().wait()
        
    except ImportError as e:
        print(f"❌ مكتبة ناقصة: {e}")
        print("📦 قم بتثبيت: pip install python-telegram-bot")
    except Exception as e:
        print(f"❌ خطأ: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # تشغيل الإيقاف أولاً
    asyncio.run(stop_other_bots())
    
    # ثم تشغيل البوت الرئيسي
    time.sleep(2)
    asyncio.run(main()) 
    
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

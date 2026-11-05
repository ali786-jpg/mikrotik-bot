import routeros_api
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- إعدادات المايكروتك ---
ROUTER_IP = "192.168.88.1"       # عنوان آي بي الراوتر الخاص بك
ROUTER_USER = "telegram_bot"     # اسم المستخدم الذي أنشأته للـ API
ROUTER_PASS = "ضع_كلمة_المرور_هنا"   # 7861102153

# --- إعدادات بوت تيليجرام ---
TOKEN = "9022753557:AAF29LUfwyqya2-oRFQW8rsGqn5dcIRtR7Q"

async def create_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("⚠️ الاستخدام الصحيح للأمر:\n/create <username> <password>")
        return

    username = args[0]
    password = args[1]

    try:
        # الاتصال بالمايكروتك عبر API
        connection = routeros_api.RouterOsApiPool(
            ROUTER_IP, 
            username=ROUTER_USER, 
            password=ROUTER_PASS, 
            plaintext_login=True
        )
        api = connection.get_api()

        # إضافة المستخدم إلى قائمة الهوتسبوت
        hotspot_users = api.get_resource('/ip/hotspot/user')
        hotspot_users.add(name=username, password=password, profile='default')
        
        connection.disconnect()
        await update.message.reply_text(f"✅ تم إنشاء حساب الهوتسبوت بنجاح!\n👤 اسم المستخدم: {username}\n🔑 كلمة المرور: {password}")
    
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء الاتصال بالراوتر أو إنشاء الحساب:\n{str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("create", create_user))
    
    print("🤖 Bot is running and connected to Mikrotik API...")
    app.run_polling()

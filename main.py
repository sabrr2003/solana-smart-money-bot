import os
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from tiktok_uploader.upload import upload_video
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- [ إعدادات البيانات الخاصة بكِ ] ---
TOKEN = "8777082488:AAFx4fw2Q0-2PvWU2ZORFiKJaDYXPpXXF-A"
MY_ID = 7992451925 

# --- [ نظام الترويج للصعود ] ---
def boost_logic(video_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # محاكاة 20 تفاعل لضمان الصعود
    for i in range(20):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(video_url)
            time.sleep(random.randint(30, 60)) # مشاهدة كاملة
            driver.quit()
        except: pass
        time.sleep(5)

# --- [ واجهة لوحة التحكم ] ---
async def start_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != MY_ID: return
    
    keyboard = [
        [InlineKeyboardButton("📤 نشر فيديو جديد", callback_data='upload')],
        [InlineKeyboardButton("🔥 ترويج رابط موجود", callback_data='promote')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً بكِ في لوحة تحكم التيك توك:\nاخري ماذا تريدين أن تفعلي الآن:", reply_markup=reply_markup)

# --- [ معالجة ضغطات الأزرار ] ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upload':
        await query.edit_message_text("حسناً، أرسلي الفيديو الآن وسأقوم بنشره وترويجه تلقائياً.")
    elif query.data == 'promote':
        context.user_data['waiting_for_link'] = True
        await query.edit_message_text("أرسلي رابط الفيديو (Link) الذي تريدين ترويجه الآن:")

# --- [ معالجة الرسائل (فيديو أو رابط) ] ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != MY_ID: return

    # حالة إرسال رابط للترويج
    if context.user_data.get('waiting_for_link'):
        url = update.message.text
        if "tiktok.com" in url:
            await update.message.reply_text("✅ تم استلام الرابط. بدأت عملية الرشق والترويج الآن...")
            boost_logic(url) # تشغيل الترويج
            context.user_data['waiting_for_link'] = False
        else:
            await update.message.reply_text("❌ عذراً، هذا ليس رابط تيك توك صحيح.")
        return

    # حالة إرسال فيديو للنشر
    if update.message.video:
        msg = await update.message.reply_text("📥 جاري التحميل والنشر...")
        video_file = await update.message.video.get_file()
        path = f"vid_{int(time.time())}.mp4"
        await video_file.download_to_drive(path)
        
        try:
            upload_video(path, description="Boosted by AI Bot 🚀 #fyp", cookies='cookies.txt')
            await msg.edit_text("✅ تم النشر بنجاح!")
        except Exception as e:
            await msg.edit_text(f"❌ فشل النشر: {str(e)}")
        if os.path.exists(path): os.remove(path)

# --- [ التشغيل ] ---
def main():
    app = Application.builder().token(TOKEN).build()
    
    # أوامر البوت
    app.add_handler(MessageHandler(filters.COMMAND, start_dashboard))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO | filters.TEXT, message_handler))
    
    print("🚀 اللوحة تعمل الآن.. أرسلي /start في تليجرام")
    app.run_polling()

if __name__ == "__main__":
    main()

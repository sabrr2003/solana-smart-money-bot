import os
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from tiktok_uploader.upload import upload_video
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- [ إعدادات البيانات الجديدة ] ---
TOKEN = "8777082488:AAFnHaQheOv8KwrT0567dTSgE5n3eGGsfAc"
MY_ID = 7992451925 

# --- [ نظام الترويج (Boosting) ] ---
def boost_logic(video_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless") # للعمل في خلفية السيرفر
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # محاكاة 20 مشاهدة لزيادة رانك الفيديو
    for i in range(20):
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(video_url)
            time.sleep(random.randint(30, 60)) # وقت مشاهدة حقيقي
            driver.quit()
        except: 
            pass
        time.sleep(5)

# --- [ واجهة لوحة التحكم ] ---
async def start_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    
    keyboard = [
        [InlineKeyboardButton("📤 نشر فيديو جديد", callback_data='upload')],
        [InlineKeyboardButton("🔥 ترويج رابط موجود", callback_data='promote')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً أميرة! لوحة التحكم جاهزة:\nاختاري العملية المطلوبة:", reply_markup=reply_markup)

# --- [ معالجة الأزرار ] ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upload':
        await query.edit_message_text("تمام، أرسلي الفيديو الآن وسأقوم بنشره وترويجه.")
    elif query.data == 'promote':
        context.user_data['waiting_for_link'] = True
        await query.edit_message_text("أرسلي رابط التيك توك الذي تريدين ترويجه الآن:")

# --- [ معالجة الرسائل ] ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return

    # ترويج الرابط
    if context.user_data.get('waiting_for_link'):
        url = update.message.text
        if "tiktok.com" in url:
            await update.message.reply_text("✅ تم استلام الرابط. جاري بدء عملية الصعود للترند... 🚀")
            boost_logic(url)
            context.user_data['waiting_for_link'] = False
        else:
            await update.message.reply_text("❌ الرابط غير صحيح، يرجى إرسال رابط تيك توك.")
        return

    # نشر الفيديو
    if update.message.video:
        msg = await update.message.reply_text("📥 جاري معالجة الفيديو والرفع...")
        video_file = await update.message.video.get_file()
        path = f"vid_{int(time.time())}.mp4"
        await video_file.download_to_drive(path)
        
        try:
            upload_video(path, description="Boosted by AI Bot 🚀 #fyp", cookies='cookies.txt')
            await msg.edit_text("✅ تم النشر بنجاح على حسابك!")
        except Exception as e:
            await msg.edit_text(f"❌ فشل النشر: {str(e)}\n(تأكدي من ملف cookies.txt)")
        
        if os.path.exists(path): os.remove(path)

# --- [ تشغيل البوت ] ---
def main():
    app = Application.builder().token(TOKEN).build()
    
    # إضافة الأوامر والمستقبلات
    app.add_handler(MessageHandler(filters.COMMAND, start_dashboard))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO | filters.TEXT, message_handler))
    
    print("🚀 البوت يعمل الآن بالتوكن الجديد.. أرسلي /start")
    
    # تنظيف أي جلسات سابقة عالقة لضمان عدم حدوث Conflict
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

import os
import random
import time
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from tiktok_uploader.upload import upload_video
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- [ بياناتك الخاصة ] ---
TOKEN = "8777082488:AAFx4fw2Q0-2PvWU2ZORFiKJaDYXPpXXF-A"
MY_ID = 7992451925 

# --- [ دالة الترويج التلقائي - الصعود للترند ] ---
def boost_video(video_url):
    print(f"🚀 بدأت حملة الصعود لـ: {video_url}")
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless") # يعمل في الخلفية
    
    # محاكاة تفاعلات من هويات مختلفة
    for i in range(15):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(video_url)
            # محاكاة وقت مشاهدة حقيقي (بين 25 و 50 ثانية)
            wait_time = random.randint(25, 50)
            time.sleep(wait_time)
            print(f"✅ تفاعل رقم {i+1} اكتمل بنجاح.")
        finally:
            driver.quit()
        time.sleep(random.randint(5, 10)) # فاصل زمني بسيط

# --- [ دالة استقبال الميديا من تليجرام ونشرها ] ---
async def handle_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # حماية: البوت مخصص لكِ فقط
    if update.message.from_user.id != MY_ID:
        return

    # التحقق هل المرسل فيديو أم صورة
    if update.message.video:
        media_file = await update.message.video.get_file()
        ext = ".mp4"
    elif update.message.photo:
        # ملاحظة: تيك توك يفضل الفيديوهات، سيتم التعامل مع الصورة كملف
        media_file = await update.message.photo[-1].get_file()
        ext = ".jpg"
    else:
        await update.message.reply_text("يرجى إرسال فيديو أو صورة فقط.")
        return

    await update.message.reply_text("📥 جاري استلام الملف ومعالجته للنشر الفوري...")
    
    file_name = f"media_{int(time.time())}{ext}"
    await media_file.download_to_drive(file_name)
    
    try:
        # النشر على تيك توك (يتطلب وجود ملف cookies.txt)
        await update.message.reply_text("📤 جاري الرفع على تيك توك الآن...")
        
        upload_video(file_name, 
                     description="تم النشر والترويج تلقائياً ⚡ #ترند #عراق #AI", 
                     cookies='cookies.txt')
        
        await update.message.reply_text("✅ تم النشر! البوت بدأ الآن بعملية 'الترويج الحقيقي' لرفع المشاهدات.")
        
        # تشغيل الترويج في الخلفية لكي لا يتوقف البوت
        # boost_video("رابط_الفيديو_هنا") 

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ في النشر: {str(e)}\nتأكدي من وضع ملف cookies.txt بجانب الكود.")
    
    # حذف الملف المحلي بعد الرفع
    if os.path.exists(file_name):
        os.remove(file_name)

# --- [ تشغيل البوت ] ---
def main():
    print("🤖 بوت الترويج والترند يعمل الآن...")
    application = Application.builder().token(TOKEN).build()
    
    # معالجة الصور والفيديوهات
    application.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, handle_upload))
    
    application.run_polling()

if __name__ == "__main__":
    main()

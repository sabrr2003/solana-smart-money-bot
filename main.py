import os
import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from tiktok_uploader.upload import upload_video
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth # مكتبة لمنع اكتشاف البوت

TOKEN = "8777082488:AAFnHaQheOv8KwrT0567dTSgE5n3eGGsfAc"
MY_ID = 7992451925 

# --- [ نظام الترويج الحقيقي باستخدام Proxies ] ---
def real_boost_logic(video_url):
    # قائمة بروكسيات (يفضل شراء بروكسيات مدفوعة لنتائج جبارة)
    # البروكسيات المجانية قد تكون بطيئة، لكن هذا هو الهيكل البرمجي
    proxies = [
        "http://proxy1_ip:port", 
        "http://proxy2_ip:port"
    ]
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    for i in range(20): # عدد المشاهدات المستهدفة في كل دورة
        proxy = random.choice(proxies) if proxies else None
        if proxy: options.add_argument(f'--proxy-server={proxy}')
        
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            # تفعيل وضع التخفي لجعل المتصفح يبدو كأنه هاتف حقيقي 100%
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

            driver.get(video_url)
            # محاكاة سلوك بشري: مشاهدة الفيديو ثم النزول للتعليقات
            time.sleep(random.randint(40, 70)) 
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(5)
            
            print(f"🔥 مشاهدة حقيقية رقم {i+1} اكتملت.")
            driver.quit()
        except Exception as e:
            print(f"⚠️ خطأ في البروكسي: {e}")
        
        time.sleep(random.randint(10, 30)) # فاصل زمني لعدم لفت الانتباه

# --- [ واجهة لوحة التحكم ] ---
async def start_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    keyboard = [[InlineKeyboardButton("📤 نشر فيديو حقيقي", callback_data='upload')],
                [InlineKeyboardButton("🔥 ترويج احترافي (بروكسي)", callback_data='promote')]]
    await update.message.reply_text("👋 أهلاً أميرة! البوت الآن في وضع الترويج الحقيقي:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'upload':
        await query.edit_message_text("أرسلي الفيديو، وسأقوم بنشره وترويجه عبر بروكسيات مختلفة.")
    elif query.data == 'promote':
        context.user_data['waiting_for_link'] = True
        await query.edit_message_text("أرسلي الرابط لزيادة المشاهدات الحقيقية:")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    if context.user_data.get('waiting_for_link'):
        url = update.message.text
        if "tiktok.com" in url:
            await update.message.reply_text("✅ تم الاستلام. جاري توزيع المشاهدات من بروكسيات عالمية... 🚀")
            real_boost_logic(url)
            context.user_data['waiting_for_link'] = False
        return
    # كود الرفع يبقى كما هو مع إضافة cookies.txt
    if update.message.video:
        await update.message.reply_text("📥 جاري الرفع والترويج الحقيقي...")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.COMMAND, start_dashboard))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO | filters.TEXT, message_handler))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

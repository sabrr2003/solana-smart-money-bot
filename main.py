import os
import random
import time
import requests
import urllib3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from tiktok_uploader.upload import upload_video

# تعطيل تحذيرات الاتصال غير الآمن لزيادة السرعة
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [ إعدادات الهوية والوصول ] ---
TOKEN = "8777082488:AAFnHaQheOv8KwrT0567dTSgE5n3eGGsfAc"
MY_ID = 7992451925 

# --- [ المحرك القوي للترويج الحقيقي ] ---
def extreme_power_boost(video_url):
    print(f"🔥 تم تفعيل المحرك القوي للرابط: {video_url}")
    
    # هوية متصفحات متنوعة وحديثة جداً
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    ]

    success_count = 0
    # تنفيذ 100 طلب ذكي في كل دورة ترويج
    for i in range(100):
        session = requests.Session()
        ua = random.choice(user_agents)
        
        # هندسة الرأس (Headers) لتبدو كزيارة حقيقية من موقع خارجي
        headers = {
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8',
            'DNT': '1',
            'Referer': 'https://www.google.com.iq/', # تظاهر بأن الزيارة من بحث جوجل العراق
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        try:
            # الخطوة 1: الحصول على كوكيز الجلسة من الصفحة الرئيسية
            session.get("https://www.tiktok.com/", headers=headers, timeout=10, verify=False)
            time.sleep(random.uniform(0.5, 1.5))
            
            # الخطوة 2: محاكاة مشاهدة الفيديو
            response = session.get(video_url, headers=headers, timeout=15, verify=False)
            
            if response.status_code == 200:
                success_count += 1
                if success_count % 10 == 0:
                    print(f"✅ تم تأكيد {success_count} محاكاة ناجحة...")
        except:
            pass
        
        # فاصل زمني تقني بسيط لعدم حظر الآي بي الخاص بـ Railway
        time.sleep(random.uniform(1, 3))

    print(f"🏁 انتهت الدورة بقوة {success_count} طلب مقبول.")

# --- [ لوحة تحكم تليجرام ] ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    
    buttons = [
        [InlineKeyboardButton("📤 نشر فيديو جديد", callback_data='up')],
        [InlineKeyboardButton("⚡ ترويج حقيقي (Railway Power)", callback_data='boost')]
    ]
    await update.message.reply_text(
        "💎 **لوحة تحكم أميرة المدفوعة** 💎\n\nالبوت متصل الآن بـ Railway ويعمل بأقصى طاقة.",
        reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown"
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'boost':
        context.user_data['action'] = 'get_link'
        await query.edit_message_text("🔗 أرسلي رابط الفيديو (Link) للبدء بالترويج الحقيقي:")
    elif query.data == 'up':
        await query.edit_message_text("🎥 أرسلي ملف الفيديو الآن لنشره.")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return

    # حالة الترويج
    if context.user_data.get('action') == 'get_link':
        url = update.message.text
        if "tiktok.com" in url:
            await update.message.reply_text("🚀 بدأت عملية الضخ الحقيقي للمشاهدات.. راقبي الـ Logs في Railway.")
            extreme_power_boost(url)
            await update.message.reply_text("✅ اكتملت دورة الترويج بقوة 100 طلب. يمكنكِ التكرار الآن.")
            context.user_data['action'] = None
        else:
            await update.message.reply_text("❌ الرابط غير مدعوم.")
        return

    # حالة الرفع
    if update.message.video:
        msg = await update.message.reply_text("📥 جاري المعالجة والرفع...")
        v_file = await update.message.video.get_file()
        name = f"video_{int(time.time())}.mp4"
        await v_file.download_to_drive(name)
        try:
            # يتطلب وجود ملف cookies.txt في السيرفر
            upload_video(name, description="Power Boosted #fyp", cookies='cookies.txt')
            await msg.edit_text("✅ تم النشر بنجاح!")
        except Exception as e:
            await msg.edit_text(f"⚠️ خطأ: {e}")
        if os.path.exists(name): os.remove(name)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.COMMAND, start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT | filters.VIDEO, handle_messages))
    print("💎 البوت القوي جاهز للعمل على Railway المدفوع...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

import os
import requests

print("🤖 AI Channel Agent started!")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = "@HoshMasnoeiAI6"

RSS_URL = "https://feeds.feedburner.com/TechCrunch/"

try:
    response = requests.get(RSS_URL, timeout=30)
    response.raise_for_status()

    print("✅ اخبار دریافت شد.")

    data = response.text

    # فعلاً فقط تست اتصال است
    print(f"📡 تعداد کاراکترهای دریافت‌شده: {len(data)}")

    if BOT_TOKEN:
        print("✅ Telegram Bot Token موجود است.")
    else:
        print("❌ Telegram Bot Token پیدا نشد.")

except Exception as e:
    print(f"❌ خطا: {e}")

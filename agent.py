import os
import requests
import xml.etree.ElementTree as ET

print("🤖 AI Channel Agent started!")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = "@HoshMasnoeiAI6"

RSS_URL = "https://feeds.feedburner.com/TechCrunch/"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": CHANNEL,
            "text": text
        },
        timeout=30
    )
    response.raise_for_status()
    print("✅ پیام با موفقیت به کانال ارسال شد.")

try:
    response = requests.get(RSS_URL, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    item = root.find(".//item")

    if item is not None:
        title = item.findtext("title", "خبر جدید")
        link = item.findtext("link", "")

        message = f"🤖 خبر هوش مصنوعی\n\n{title}\n\n🔗 {link}"
        send_message(message)
    else:
        print("❌ خبری پیدا نشد.")

except Exception as e:
    print(f"❌ خطا: {e}")

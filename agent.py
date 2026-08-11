import os
import requests
import xml.etree.ElementTree as ET

print("🤖 AI Channel Agent started!")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = "@HoshMasnoeiAI6"

RSS_SOURCES = [
    "https://openai.com/news/rss.xml",
    "https://blog.google/innovation-and-ai/rss/",
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={"chat_id": CHANNEL, "text": text},
        timeout=30
    )
    response.raise_for_status()
    print("✅ پیام منتشر شد.")

for rss_url in RSS_SOURCES:
    try:
        response = requests.get(rss_url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        item = root.find(".//item")

        if item is not None:
            title = item.findtext("title", "خبر جدید")
            link = item.findtext("link", "")

            message = f"🤖 هوش مصنوعی\n\n{title}\n\n🔗 {link}"
            send_message(message)
            break

    except Exception as e:
        print(f"⚠️ منبع در دسترس نبود: {e}")

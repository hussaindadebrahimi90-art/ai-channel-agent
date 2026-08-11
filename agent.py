import os
import requests
import xml.etree.ElementTree as ET
import hashlib

print("🤖 AI Channel Agent started!")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = "@HoshMasnoeiAI6"

RSS_SOURCES = [
    "https://openai.com/news/rss.xml",
    "https://blog.google/feed/",
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

def get_item(rss_url):
    response = requests.get(rss_url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    item = root.find(".//item")

    if item is None:
        return None

    title = item.findtext("title", "خبر جدید").strip()
    link = item.findtext("link", "").strip()

    return title, link

try:
    for rss_url in RSS_SOURCES:
        try:
            item = get_item(rss_url)

            if item:
                title, link = item

                message = (
                    f"🤖 هوش مصنوعی\n\n"
                    f"{title}\n\n"
                    f"🔗 {link}"
                )

                send_message(message)
                break

        except Exception as e:
            print(f"⚠️ خطا در منبع: {e}")

except Exception as e:
    print(f"❌ خطای Agent: {e}")

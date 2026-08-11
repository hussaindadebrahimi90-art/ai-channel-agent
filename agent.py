import os
import requests
import xml.etree.ElementTree as ET
from google import genai

print("🤖 AI Channel Agent started!")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL = "@HoshMasnoeiAI6"

RSS_SOURCES = [
    "https://openai.com/news/rss.xml",
    "https://blog.google/feed/",
]

client = genai.Client(api_key=GEMINI_API_KEY)


def get_news(rss_url):
    response = requests.get(rss_url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    item = root.find(".//item")

    if item is None:
        return None

    title = item.findtext("title", "خبر جدید").strip()
    link = item.findtext("link", "").strip()

    return title, link


def summarize_with_gemini(title):
    prompt = f"""
عنوان خبر:
{title}

این خبر را برای یک کانال فارسی هوش مصنوعی آماده کن.

قوانین:
- عنوان را به فارسی روان ترجمه کن.
- یک خلاصه کوتاه 2 تا 3 خطی بنویس.
- اطلاعات جدیدی اضافه نکن.
- لحن حرفه‌ای و ساده باشد.
- فقط متن فارسی را برگردان.

فرمت:

📰 [عنوان فارسی]

📝 [خلاصه فارسی]
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHANNEL,
            "text": text,
        },
        timeout=30,
    )

    response.raise_for_status()
    print("✅ پیام در کانال منتشر شد.")


for rss_url in RSS_SOURCES:
    try:
        news = get_news(rss_url)

        if news:
            title, link = news

            print(f"📰 خبر پیدا شد: {title}")

            translated = summarize_with_gemini(title)

            message = (
                f"{translated}\n\n"
                f"🔗 منبع: {link}"
            )

            send_message(message)
            break

    except Exception as e:
        print(f"⚠️ خطا: {e}")

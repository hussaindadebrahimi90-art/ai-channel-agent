import os
import json
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

MEMORY_FILE = "posted.json"

client = genai.Client(api_key=GEMINI_API_KEY)


def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return set(data)

    except Exception:
        pass

    return set()


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            sorted(memory),
            f,
            ensure_ascii=False,
            indent=2
        )


def get_news(rss_url):
    response = requests.get(rss_url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    item = root.find(".//item")

    if item is None:
        return None

    title = item.findtext("title", "").strip()
    link = item.findtext("link", "").strip()

    if not title or not link:
        return None

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


memory = load_memory()

print(f"🧠 تعداد خبرهای ذخیره‌شده: {len(memory)}")


for rss_url in RSS_SOURCES:

    try:

        news = get_news(rss_url)

        if not news:
            continue

        title, link = news

        print(f"📰 خبر پیدا شد: {title}")
        print(f"🔗 لینک: {link}")

        if link in memory:
            print("⏭️ این خبر قبلاً منتشر شده است.")
            continue

        print("🆕 خبر جدید است.")

        translated = summarize_with_gemini(title)

        message = (
            f"{translated}\n\n"
            f"🔗 منبع: {link}"
        )

        send_message(message)

        memory.add(link)
        save_memory(memory)

        print("💾 خبر در حافظه ذخیره شد.")

        break

    except Exception as e:

        print(f"⚠️ خطا در منبع {rss_url}: {e}")

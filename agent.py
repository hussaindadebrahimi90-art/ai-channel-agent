import os
import requests

print("🤖 AI Channel Agent started!")

# تست دریافت اخبار هوش مصنوعی از RSS
RSS_URL = "https://www.artificialintelligence-news.com/feed/"

response = requests.get(RSS_URL, timeout=20)

if response.status_code == 200:
    print("✅ منبع اخبار با موفقیت دریافت شد.")
    print("📡 Agent آماده دریافت محتوا است.")
else:
    print("❌ دریافت منبع ناموفق بود.")

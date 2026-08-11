import requests

print("🤖 AI Channel Agent started!")

RSS_URL = "https://feeds.feedburner.com/TechCrunch/"

try:
    response = requests.get(RSS_URL, timeout=30)

    if response.status_code == 200:
        print("✅ منبع اخبار با موفقیت دریافت شد.")
        print("📡 Agent آماده دریافت محتوا است.")
    else:
        print(f"❌ خطای منبع: {response.status_code}")

except requests.RequestException as e:
    print(f"❌ خطا در اتصال: {e}")

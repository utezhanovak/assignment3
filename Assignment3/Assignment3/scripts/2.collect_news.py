

import requests
import pandas as pd
import time
import os

API_TOKEN = "4612f1d6eac6a2512b316a6bb6b09475ab66fb23"
CURRENCIES = "BTC,ETH,USDT,BNB,SOL,XRP,USDC,ADA,AVAX,DOGE"

news_data = []
headers = {"Accept": "application/json"}

os.makedirs("data", exist_ok=True)

print("⏳ Testing API with just 1 page...")
for page in range(1, 2):
    print(f"📄 Fetching page {page}...")
    params = {
        "auth_token": API_TOKEN,
        "public": "true",
        "currencies": CURRENCIES,
        "kind": "news",
        "page": page
    }
    try:
        response = requests.get("https://cryptopanic.com/api/v1/posts/", params=params, headers=headers, timeout=10)
        print("✅ Response received")
        if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
            posts = response.json()["results"]
            print(f"📥 {len(posts)} posts found on page {page}")
            for post in posts:
                news_data.append({
                    "date": post["published_at"][:10],
                    "title": post["title"],
                    "currencies": ",".join([c["code"] for c in post.get("currencies", [])]) if post.get("currencies") else "UNKNOWN"
                })
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching page {page}: {e}")

df = pd.DataFrame(news_data)
df.to_csv("data/news/crypto_news_titles.csv", index=False)
print("✅ News titles saved to 'data/news/crypto_news_titles.csv'")


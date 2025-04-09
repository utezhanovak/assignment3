import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

df = pd.read_csv("data/news/crypto_news_titles.csv")

analyzer = SentimentIntensityAnalyzer()

df["sentiment"] = df["title"].apply(lambda x: analyzer.polarity_scores(str(x))["compound"])

df["date"] = pd.to_datetime(df["date"])
rows = []

for _, row in df.iterrows():
    coins = row["currencies"].split(",")
    for coin in coins:
        rows.append({
            "Date": row["date"],
            "coin": coin.strip().upper(),
            "sentiment": row["sentiment"]
        })

sentiment_df = pd.DataFrame(rows)
daily_sentiment = sentiment_df.groupby(["Date", "coin"]).mean().reset_index()
daily_sentiment = daily_sentiment.rename(columns={"sentiment": "avg_sentiment"})

os.makedirs("data", exist_ok=True)
daily_sentiment.to_csv("data/daily_coin_sentiment.csv", index=False)
print("✅ Sentiment scores saved to 'data/daily_coin_sentiment.csv'")

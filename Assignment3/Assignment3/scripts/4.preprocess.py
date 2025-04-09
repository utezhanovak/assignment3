import os
import pandas as pd
import numpy as np

coins_folder = "data/coins"
all_prices = []

for file in os.listdir(coins_folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(coins_folder, file))
        all_prices.append(df)

df_prices = pd.concat(all_prices)
df_prices["Date"] = pd.to_datetime(df_prices["Date"])
df_prices["coin"] = df_prices["coin"].str.upper().str.replace("-", "")

df_news = pd.read_csv("data/news/crypto_news_titles.csv")
df_news["date"] = pd.to_datetime(df_news["date"])
df_news["currencies"] = df_news["currencies"].str.upper()

np.random.seed(42)
df_news["sentiment"] = np.random.choice([-1, 0, 1], size=len(df_news))

df_news["currencies"] = df_news["currencies"].str.split(",")
df_exploded = df_news.explode("currencies").rename(columns={"currencies": "coin"})

df_sentiment = df_exploded.groupby(["date", "coin"])["sentiment"].mean().reset_index()
df_sentiment = df_sentiment.rename(columns={"date": "Date", "sentiment": "avg_sentiment"})

df_merged = pd.merge(df_prices, df_sentiment, how="left", on=["Date", "coin"])
df_merged["avg_sentiment"] = df_merged["avg_sentiment"].fillna(0)

df_merged = df_merged.sort_values(["coin", "Date"])
df_merged.to_csv("data/final_model_data.csv", index=False)

print("✅ Preprocessing complete. Data saved to 'data/final_model_data.csv'")

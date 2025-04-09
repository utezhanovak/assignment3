import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

model_data = pd.read_csv("data/model_input_data.csv")
predictions = pd.read_csv("data/predictions/next_day_predictions.csv")

model_data["Date"] = pd.to_datetime(model_data["Date"])

os.makedirs("plots", exist_ok=True)

for coin in model_data["coin"].unique():
    coin_df = model_data[model_data["coin"] == coin]
    plt.figure()
    plt.plot(coin_df["Date"], coin_df["Close"])
    plt.title(f"{coin} Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Close Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"plots/{coin}_price_trend.png")
    plt.close()

plt.figure(figsize=(10, 6))
for coin in model_data["coin"].unique():
    df = model_data[model_data["coin"] == coin]
    plt.scatter(df["lag_sentiment"], df["return"], alpha=0.6, label=coin)

plt.title("Sentiment vs. Return")
plt.xlabel("Lagged Sentiment")
plt.ylabel("Return")
plt.legend(fontsize="small", bbox_to_anchor=(1.05, 1))
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/sentiment_vs_return.png")
plt.close()

plt.figure(figsize=(10, 6))

x = np.arange(len(predictions))
width = 0.35

plt.bar(x - width / 2, predictions["today_price"], width=width, label="Today")
plt.bar(x + width / 2, predictions["predicted_price"], width=width, label="Predicted")

plt.yscale("log")  
plt.xticks(x, predictions["coin"], rotation=45)
plt.title("Today vs Predicted Price (Next Day)")
plt.ylabel("Price (USD, log scale)")
plt.legend()
plt.tight_layout()
plt.savefig("plots/predicted_vs_actual.png")
plt.close()

print("✅ Visualizations saved in the 'plots/' folder.")

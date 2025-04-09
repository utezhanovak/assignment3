import pandas as pd
import os

df = pd.read_csv("data/model_input_data.csv")

latest_sentiment = df.sort_values("Date").groupby("coin").tail(1)[["coin", "Close", "avg_sentiment"]]
latest_sentiment = latest_sentiment.set_index("coin")

model_df = pd.read_csv("data/model_evaluation.csv")
model_df = model_df.set_index("coin")

results = []

for coin in model_df.index:
    if coin not in latest_sentiment.index:
        print(f"⚠️ No sentiment or price found for {coin}")
        continue

    today_price = latest_sentiment.loc[coin, "Close"]
    sentiment = latest_sentiment.loc[coin, "avg_sentiment"]
    coef = model_df.loc[coin, "coef"]
    intercept = model_df.loc[coin, "intercept"]

    predicted_return = coef * sentiment + intercept
    predicted_price = today_price * (1 + predicted_return)

    results.append({
        "coin": coin,
        "today_price": today_price,
        "predicted_return": predicted_return,
        "predicted_price": predicted_price
    })

predictions_df = pd.DataFrame(results)
print("📈 Predictions for next day:")
print(predictions_df)

os.makedirs("data/predictions", exist_ok=True)
predictions_df.to_csv("data/predictions/next_day_predictions.csv", index=False)

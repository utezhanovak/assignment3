import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

os.makedirs("data", exist_ok=True)

price_files = [f"data/coins/{file}" for file in os.listdir("data/coins") if file.endswith(".csv")]
dfs = []

for file in price_files:
    df = pd.read_csv(file)
    df["coin"] = df["coin"].str.upper()
    df["Date"] = pd.to_datetime(df["Date"])
    dfs.append(df)

df = pd.concat(dfs)
df = df.sort_values(["coin", "Date"])

sentiment_df = pd.read_csv("data/daily_coin_sentiment.csv")
sentiment_df["Date"] = pd.to_datetime(sentiment_df["Date"])
sentiment_df["coin"] = sentiment_df["coin"].str.upper()

df_model = pd.merge(df, sentiment_df, on=["Date", "coin"], how="left")
df_model["avg_sentiment"] = pd.to_numeric(df_model["avg_sentiment"], errors="coerce").fillna(0)

df_model["Close"] = pd.to_numeric(df_model["Close"], errors="coerce")
df_model["return"] = df_model.groupby("coin")["Close"].pct_change()
df_model["lag_sentiment"] = df_model.groupby("coin")["avg_sentiment"].shift(1)
df_model.dropna(subset=["return", "lag_sentiment"], inplace=True)

df_model.to_csv("data/model_input_data.csv", index=False)
print("✅ Model input data saved.")

results = []

for coin in df_model["coin"].unique():
    coin_df = df_model[df_model["coin"] == coin]

    X = coin_df[["lag_sentiment"]]
    y = coin_df["return"]

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    results.append({
        "coin": coin,
        "r2_score": r2_score(y, y_pred),
        "coef": model.coef_[0],
        "intercept": model.intercept_
    })

df_results = pd.DataFrame(results)
df_results.to_csv("data/model_evaluation.csv", index=False)

print("📊 Evaluation Results:")
print(df_results)

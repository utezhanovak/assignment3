import yfinance as yf
import pandas as pd
import os

os.makedirs("data/coins", exist_ok=True)

COINS = {
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",
    "tether": "USDT-USD",
    "binancecoin": "BNB-USD",
    "solana": "SOL-USD",
    "ripple": "XRP-USD",
    "usd-coin": "USDC-USD",
    "cardano": "ADA-USD",
    "avalanche-2": "AVAX-USD",
    "dogecoin": "DOGE-USD"
}

start_date = "2023-01-01"
end_date = "2024-12-31"

for name, ticker in COINS.items():
    print(f"⬇ Downloading {name}")
    df = yf.download(ticker, start=start_date, end=end_date, progress=False).reset_index()
    df["coin"] = name
    df.to_csv(f"data/coins/{name}.csv", index=False)

print("✅ Price data saved")

## Objective

Predict the next-day price movement of cryptocurrencies using:
- 📈 Historical prices (2023–2024)
- 📰 Crypto news titles (from [CryptoPanic](https://cryptopanic.com/))
- 💬 Sentiment analysis

## Features Implemented

- ✅ Top 10 crypto data collection from yFinance
- ✅ News title collection from CryptoPanic API
- ✅ Title-based sentiment scoring (VADER)
- ✅ Aggregated daily coin-level sentiment
- ✅ Linear regression model per coin
- ✅ Next-day price prediction using lagged sentiment
- ✅ Visualizations: trends, sentiment vs return, prediction bars

## ML Approach

- Model: Linear Regression
- Features: Previous day sentiment score
- Target: Next-day return
- Output: `next_day_predictions.csv` (with predicted price)

## How to Run

pip install -r requirements.txt

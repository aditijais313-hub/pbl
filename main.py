import streamlit as st
from data_fetch import fetch_news
from sentiment import analyze_sentiment
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="FinSight", layout="wide")

st.title("📊 FinSight - Financial News Sentiment Analyzer")

query = st.text_input("Enter Topic (e.g., Tesla, RBI, Inflation):", "stock market")

if st.button("Analyze"):
    news = fetch_news(query)

    results = []

    for article in news[:10]:
        label, score = analyze_sentiment(article)
        results.append({
            "News": article,
            "Sentiment": label,
            "Confidence": round(score, 2)
        })

    df = pd.DataFrame(results)

    st.subheader("News Sentiment Results")
    st.write(df)

    st.subheader("Sentiment Distribution")
    st.bar_chart(df["Sentiment"].value_counts())

    st.subheader("Stock Trend (AAPL Example)")
    stock = yf.download("AAPL", period="5d")
    st.line_chart(stock["Close"])
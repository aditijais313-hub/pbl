import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.express as px
import streamlit as st

import config
from news_fetcher import fetch_financial_news
from sentiment import analyze_headline_sentiment, load_finbert_pipeline
from stock_data import get_stock_history

st.set_page_config(page_title="FinSight - Sentiment Dashboard", layout="wide")
st.title("📊 FinSight: Financial News Sentiment Analyzer")

try:
    secret_key = st.secrets.get("NEWS_API_KEY", "")
except Exception:
    secret_key = ""
default_key = secret_key or config.NEWS_API_KEY

ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, NVDA, TSLA):", "AAPL").strip().upper()
api_key = st.sidebar.text_input(
    "NewsAPI Key (optional):", value=default_key, type="password",
    help="Leave blank to use Yahoo Finance news instead.",
)
period = st.sidebar.selectbox("Price history", ["5d", "1mo", "3mo", "6mo", "1y"], index=1)

if st.sidebar.button("Run Analysis", type="primary"):
    if not ticker:
        st.error("Please enter a ticker.")
        st.stop()

    with st.spinner("Loading FinBERT (first run downloads ~440MB)..."):
        analyzer = load_finbert_pipeline()

    with st.spinner("Fetching news..."):
        try:
            news, source = fetch_financial_news(ticker, api_key, config.MAX_ARTICLES)
        except Exception as e:
            st.error(f"Could not fetch news: {e}")
            st.stop()

    if not news:
        st.warning("No news found for that ticker.")
        st.stop()

    with st.spinner("Analyzing sentiment..."):
        sentiment_data = analyze_headline_sentiment(news, analyzer)

    try:
        stock_df = get_stock_history(ticker, period)
    except Exception:
        stock_df = pd.DataFrame()

    st.caption(f"News source: {source} · {len(sentiment_data)} headlines analyzed")
    df_sent = pd.DataFrame(sentiment_data)

    net = (df_sent["positive"] - df_sent["negative"]).mean()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Net sentiment", f"{net:+.2f}")
    m2.metric("Positive", int((df_sent.sentiment == "positive").sum()))
    m3.metric("Neutral", int((df_sent.sentiment == "neutral").sum()))
    m4.metric("Negative", int((df_sent.sentiment == "negative").sum()))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Recent Sentiment for {ticker}")
        fig_pie = px.pie(
            df_sent, names="sentiment", title="Sentiment Distribution", color="sentiment",
            color_discrete_map={"positive": "green", "neutral": "gray", "negative": "red"},
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader(f"{ticker} Stock Price Movement")
        if stock_df.empty:
            st.info("No price data available for this ticker.")
        else:
            fig_line = px.line(stock_df, x="Date", y="Close", title=f"{ticker} Closing Price")
            st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Analyzed News Headlines")
    icons = {"positive": "🟢", "negative": "🔴", "neutral": "⚪"}
    for item in sentiment_data:
        link = f"[{item['title']}]({item['url']})" if item["url"] else item["title"]
        st.markdown(f"**{icons[item['sentiment']]} {link}** — *{item['sentiment']}, confidence {item['confidence']:.2f}*")
else:
    st.info("Enter a ticker in the sidebar and click **Run Analysis**.")

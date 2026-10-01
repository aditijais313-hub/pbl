import streamlit as st
from transformers import pipeline

MODEL_NAME = "ProsusAI/finbert"


@st.cache_resource(show_spinner=False)
def load_finbert_pipeline():
    # top_k=None returns scores for all three labels (replaces deprecated return_all_scores)
    return pipeline("text-classification", model=MODEL_NAME, top_k=None)


def analyze_headline_sentiment(news_list, analyzer):
    items = [n for n in news_list if n.get("title")]
    if not items:
        return []

    outputs = analyzer([n["title"] for n in items], batch_size=16, truncation=True, max_length=128)

    results = []
    for item, scores in zip(items, outputs):
        score_dict = {r["label"].lower(): r["score"] for r in scores}
        top = max(score_dict, key=score_dict.get)
        results.append(
            {
                "title": item["title"],
                "sentiment": top,
                "confidence": score_dict[top],
                "positive": score_dict.get("positive", 0.0),
                "neutral": score_dict.get("neutral", 0.0),
                "negative": score_dict.get("negative", 0.0),
                "url": item.get("url", ""),
                "publishedAt": item.get("publishedAt"),
            }
        )
    return results

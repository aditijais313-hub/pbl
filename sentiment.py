from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    
    label = result["label"]
    score = result["score"]
    
    return label, score
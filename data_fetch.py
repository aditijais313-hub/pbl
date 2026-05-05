import requests

API_KEY = "YOUR_API_KEY"

def fetch_news(query="stock market"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}&language=en"
    response = requests.get(url)
    data = response.json()
    
    articles = []
    for article in data.get("articles", []):
        articles.append(article["title"])
    
    return articles
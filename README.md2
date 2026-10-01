# FinSight – Financial News Sentiment Analyzer

Fetches recent headlines for a stock, scores them with FinBERT (ProsusAI/finbert), and plots sentiment next to price history.

## Run
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```
Open http://localhost:8501. A NewsAPI key is optional; without one, Yahoo Finance news is used.
To preload a key, create `.env` with `NEWS_API_KEY=your_key`.

## Deploy (Streamlit Community Cloud)
Push to GitHub, create an app with `app/main.py` as the entry file, and add `NEWS_API_KEY = "..."` under Advanced settings > Secrets.

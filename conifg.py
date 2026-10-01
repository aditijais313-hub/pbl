"""API keys and constants. Put NEWS_API_KEY in a .env file or Streamlit secrets."""
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
MODEL_NAME = "ProsusAI/finbert"
MAX_ARTICLES = 15

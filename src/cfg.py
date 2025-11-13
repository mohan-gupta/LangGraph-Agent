import os

from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_cluster_url = os.getenv("QDRANT_CLUSTER_URL")
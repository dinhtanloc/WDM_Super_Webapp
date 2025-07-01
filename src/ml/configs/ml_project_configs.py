# src/ml/app/config/config.py

import os
from dotenv import load_dotenv, find_dotenv

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_KEY = os.getenv("QDRANT_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class Settings:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.QDRANT_HOST = os.getenv("QDRANT_HOST")

        self.NEO4J_URI = os.getenv("NEO4J_URI")
        self.NEO4J_USER = os.getenv("NEO4J_USERNAME")
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

        self.MLFLOW_TRACKING_URI = os.getenv("MLFLOW_URI")

        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()

# src/ml/app/config/config.py

import os
from dotenv import load_dotenv, find_dotenv

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

"""
Configuration for the finnhub_historical database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class FinnhubHistoricalDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('FINNHUB_HISTORICAL_DB_URI')

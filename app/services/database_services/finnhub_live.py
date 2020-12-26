"""
Configuration for the finnhub_live database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class FinnhubLiveDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('FINNHUB_LIVE_DB_URI')

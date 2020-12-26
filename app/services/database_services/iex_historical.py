"""
Configuration for the iex_historical database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class IexHistoricalDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('IEX_HISTORICAL_DB_URI')

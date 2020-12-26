"""
Configuration for the tokyo_commodities_historical database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class TokyoCommoditiesHistoricalDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('TOKYO_COMMODITIES_HISTORICAL_DB_URI')

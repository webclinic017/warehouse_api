"""
Configuration for the nomics_historical database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class NomicsHistoricalDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('NOMICS_HISTORICAL_DB_URI')

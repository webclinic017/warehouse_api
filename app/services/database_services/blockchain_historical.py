"""
Configuration for the blockchain_historical database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class BlockchainHistoricalDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('BLOCKCHAIN_HISTORICAL_DB_URI')

"""
Configuration for the blockchain_live database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class BlockchainLiveDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('BLOCKCHAIN_LIVE_DB_URI')

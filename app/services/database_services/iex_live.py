"""
Configuration for the iex_live database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class IexLiveDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('IEX_LIVE_DB_URI')

"""
Configuration for the nomics_live database
"""
import os
from app.abstract.services.database_service.config import DatabaseConnectionConfig


class NomicsLiveDbConfig(DatabaseConnectionConfig):
    db_uri: str = os.environ.get('NOMICS_LIVE_DB_URI')

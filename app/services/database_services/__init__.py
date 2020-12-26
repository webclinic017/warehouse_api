"""
Module to host all database connections
"""
from .nomics_live import NomicsLiveDbConfig

DB_CONFIGS = [
    NomicsLiveDbConfig()
]

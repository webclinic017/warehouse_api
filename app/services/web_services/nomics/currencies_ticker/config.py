"""
Module containing the configuration for the nomics/currencies_ticker microservice
"""
from app.abstract.services.database_service.config import (
    DbQueryConfig,
    DatabaseConnectionConfig,
)
from app.services.database_services.nomics_live import NomicsLiveDbConfig

currencies_ticker_sql = """
SELECT *
FROM currencies.currencies_ticker
"""
currencies_ticker_db_query_label = "nomics_currencies_ticker"


class NomicsCurrenciesTickerDbQueryConfig(DbQueryConfig):
    label: str = currencies_ticker_db_query_label
    sql: str = currencies_ticker_sql
    db_config: DatabaseConnectionConfig = NomicsLiveDbConfig()

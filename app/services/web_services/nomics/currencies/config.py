"""
Module containing the configuration for the nomics/currencies microservice
"""
from app.abstract.services.database_service.config import (
    DbQueryConfig,
    DatabaseConnectionConfig,
)
from app.services.database_services.nomics_live import NomicsLiveDbConfig

currencies_sql = """
SELECT *
FROM currencies.currencies
"""
currencies_db_query_label = "nomics_currencies"


class NomicsCurrenciesDbQueryConfig(DbQueryConfig):
    label: str = currencies_db_query_label
    sql: str = currencies_sql
    db_config: DatabaseConnectionConfig = NomicsLiveDbConfig()

"""
Module containing the configuration for the tokyo_commodities_exchange/quotes_by_day_session microservice
"""
from app.abstract.services.database_service.config import (
    DbQueryConfig,
    DatabaseConnectionConfig,
)
from app.services.database_services.tokyo_commodities_historical import TokyoCommoditiesHistoricalDbConfig

quotes_by_day_session_sql = """
SELECT *
FROM downloads.quotes_by_day_session
"""
quotes_by_day_session_db_query_label = "tokyo_commodities_exchange_quotes_by_day_session"


class QuotesByDaySessionDbQueryConfig(DbQueryConfig):
    label: str = quotes_by_day_session_db_query_label
    sql: str = quotes_by_day_session_sql
    db_config: DatabaseConnectionConfig = TokyoCommoditiesHistoricalDbConfig()

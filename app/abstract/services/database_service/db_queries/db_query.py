from concurrent.futures.thread import ThreadPoolExecutor
from typing import Optional

from app.abstract.services.database_service.config import DbQueryConfig, DbQueryReturnType, DbQueryRunOptions, \
    MAX_WORKER_THREADS, THREAD_NAME_PREFIX
from app.abstract.services.database_service.db_connection import DatabaseConnection
from app.abstract.services.database_service.db_queries.regex_constants import REGEX_FOR_ORDER
from app.abstract.services.database_service.db_queries.utils import split_sql_statement_around_pattern, \
    append_where_clause, append_pagination_clause


class DbQuery:
    """
    Base class for all Database queries that has a database session and an sql query
    """

    def __init__(self, config: DbQueryConfig):
        self.config = config
        self.label = config.label
        self.sql_split_around_order = split_sql_statement_around_pattern(
            sql_statement=config.sql, compiled_pattern=REGEX_FOR_ORDER, replacement_clause='ORDER BY')

    def __get_sql(self, limit: int = None, offset: int = None, q: Optional[str] = None):
        left_sql_fragment, right_sql_fragment = self.sql_split_around_order
        left_sql_fragment = append_where_clause(sql_statement=left_sql_fragment, where_clause=q)
        sql = f"{left_sql_fragment} {right_sql_fragment}"
        sql = append_pagination_clause(sql_statement=sql, limit=limit, offset=offset)
        return sql

    def run(self, options: DbQueryRunOptions = DbQueryRunOptions()) -> DbQueryReturnType:
        """Runs a given query and returns the database records"""
        query = options.params.get("q", options.q)

        with DatabaseConnection(db_connection_config=self.config.db_config) as db:
            records_sql: str = self.__get_sql(limit=options.limit, offset=options.offset, q=query)
            records_result_proxy = db.execute_sql(sql=records_sql, params=options.params)

            count_result_proxy = None
            result = DbQueryReturnType()
            records_fetch_method: str = 'first'

            if options.should_fetch_total:
                totals_sql = self.__get_sql(q=query)
                count_result_proxy = db.execute_sql(sql=totals_sql, params=options.params)

            if options.multiple_records:
                records_fetch_method = 'fetchall'

            with ThreadPoolExecutor(max_workers=MAX_WORKER_THREADS / 2,
                                    thread_name_prefix=THREAD_NAME_PREFIX) as executor:
                task_for_records = executor.submit(getattr(records_result_proxy, records_fetch_method))

                if count_result_proxy is not None:
                    result.total = executor.submit(lambda: count_result_proxy.rowcount).result()

                result.data = task_for_records.result()

            return result

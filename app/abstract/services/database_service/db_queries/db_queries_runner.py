from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Callable, Dict, Any

from app.abstract.services.database_service.config import DbQueryConfig, DbQueryReturnType, DbQueryRunOptions, \
    MAX_WORKER_THREADS, THREAD_NAME_PREFIX
from app.abstract.services.database_service.db_queries.db_query import DbQuery
from app.abstract.services.database_service.db_queries.utils import extract_sql_param_from_http_param


class DbQueriesRunner:
    """
    Base class for all DB Query runners that receive a list of dbQueries,
    and runs them and returns a single set of records from the given dict
    """

    def __init__(self, configs: List[DbQueryConfig],
                 db_query_results_merger: Callable[[Dict[str, DbQueryReturnType]], DbQueryReturnType]):
        super().__init__()

        db_queries_list: List[DbQuery] = [DbQuery(config) for config in configs]
        self.db_queries: Dict[str, DbQuery] = {
            db_query.label: db_query for db_query in db_queries_list
        }
        self.db_query_results_merger = db_query_results_merger
        self.__query_param_separator = "__"

    def _get_params_for_each_db_query(self, params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Extracts the params for each DbQuery in the list of DbQueries from a dict of parameters
        Assumption: parameters are of pattern <DbQuery.label>__<query_name>
        example: {'da_ndf__q': 'WHERE a.sp_uk = 9'} becomes {'da_ndf': {'q': 'WHERE a.sp_uk = 9'}
        """
        params_for_each_db_query = {}
        separator = self.__query_param_separator

        for param, value in params.items():
            db_query_label, query_name = extract_sql_param_from_http_param(
                separator=separator, http_param=param)

            params_for_each_db_query.setdefault(db_query_label, {})
            params_for_each_db_query[db_query_label][query_name] = value

        return params_for_each_db_query

    def run(self, options: DbQueryRunOptions) -> DbQueryReturnType:
        """
        Runs the db queries and then merges the results using the db_query_results_merger property
        """
        params_map = self._get_params_for_each_db_query(options.params)

        result_dict = {
            label: db_query.run(DbQueryRunOptions(**{**options.dict(), 'params': params_map.get(label, {})}))
            for label, db_query in self.db_queries.items()
        }

        return self.db_query_results_merger(result_dict)

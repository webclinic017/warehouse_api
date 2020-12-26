"""
Module to house the microservice abstract class
"""
from asyncio import sleep
from typing import Union, List, Dict, Callable, Optional, Type
from abc import ABC, abstractmethod

import sqlalchemy.engine as sqlalchemy_engine
from fastapi import WebSocket
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect

from app.abstract.config import is_testing
from app.abstract.services.database_service.config import DbQueryConfig, DbQueryReturnType, DbQueryRunOptions
from app.abstract.services.database_service.db_queries import DbQuery
from app.abstract.services.database_service.db_queries.db_queries_runner import DbQueriesRunner
from app.abstract.web_servers.websocket import WebsocketConnectionManager

_ROW_PROXY = sqlalchemy_engine.RowProxy


class ReadOnlyMicroservice(ABC):
    """
    Retrieves data from a request and calls
    a corresponding db_query or db_queries_runner
    Create a class based view using fastapi-utils as shown in the link below
    https://fastapi-utils.davidmontague.xyz/user-guide/class-based-views/
    """

    def __init__(self, config: Union[DbQueryConfig, List[DbQueryConfig]],
                 db_query_results_merger: Callable[[Dict[str, DbQueryReturnType]], DbQueryReturnType] = None):
        super().__init__()

        if isinstance(config, DbQueryConfig):
            self.db_query = DbQuery(config)

        elif db_query_results_merger is None:
            raise Exception(
                "db_query_results_merger should be defined for microservices with multiple DbQuery's")
        else:
            self.db_query = DbQueriesRunner(
                configs=config, db_query_results_merger=db_query_results_merger)

    def __get_records(self, options: DbQueryRunOptions) -> DbQueryReturnType:
        """
        sql statement of form 'select * from table_this where "column_1" = %(column_1_value)'
        and the params would be {"column_1_value": 9}
        """
        return self.db_query.run(options=options)

    def _list(self, limit: int = None, offset: int = None, q: str = None,
              should_fetch_total=True, *args, **kwargs) -> DbQueryReturnType:
        """
        Returns a list of items when called. Disable in child class using pass if not needed
        """
        list_options = DbQueryRunOptions(
            limit=limit, offset=offset, q=q, should_fetch_total=should_fetch_total,
            multiple_records=True, params=kwargs)

        return self.__get_records(options=list_options)

    def _get_one(self, q: str = None, *args, **kwargs) -> DbQueryReturnType:
        """
        Returns a single item from the result proxy. Disable in child using pass not needed
        """
        single_record_options = DbQueryRunOptions(
            **{'q': q, 'params': kwargs, 'multiple_records': False, 'should_fetch_total': False})

        return self.__get_records(options=single_record_options)

    async def websocket_list(self, websocket: WebSocket, response_model: Type[BaseModel],
                             q: Optional[str] = None, limit: int = None, *args, **kwargs):
        """Returns the list view but as a repetitive websocket response"""
        path = f'{websocket.url}?q={q}&limit={limit}&args={args}&kwargs={kwargs}'
        await WebsocketConnectionManager.connect(websocket=websocket, path=path)

        try:
            while True:
                raw_data = self.list(q=q, limit=limit, *args, **kwargs)
                raw_data['data'] = [dict(datum) for datum in raw_data['data']]

                data = response_model.parse_obj(raw_data).json()
                await WebsocketConnectionManager.send(message=data, websocket=websocket)

                if is_testing():
                    await websocket.close()
                    break

                await sleep(WebsocketConnectionManager.sleep_interval)

        except WebSocketDisconnect:
            WebsocketConnectionManager.disconnect(websocket=websocket, path=path)

    @abstractmethod
    def list(self, limit: int = None, *args, **kwargs):
        """
        Override this method to return a list of items
        """
        raise NotImplementedError(
            'The list method should be implemented. Call the self._list method here')

    @abstractmethod
    def get_one(self, *args, **kwargs):
        """
        Override this method to return a single item of the resource
        """
        raise NotImplementedError(
            'The get_one method should be implemented. You may call the self._get_one method here')

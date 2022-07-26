"""
Module containing the quotes_by_day_session microservice
"""
from datetime import date, time
from typing import Optional, Dict

from app.abstract.services.web_service.config import MicroserviceConfig, MicroserviceListResponse
from app.abstract.services.web_service.readonly_microservice import ReadOnlyMicroservice
from fastapi import APIRouter, Query, WebSocket
from fastapi_utils.cbv import cbv

from .config import QuotesByDaySessionDbQueryConfig

quotes_by_day_session_router = APIRouter()
microservice_config = MicroserviceConfig()


@cbv(quotes_by_day_session_router)
class QuotesByDaySessionMicroservice(ReadOnlyMicroservice):
    """
    Returns data for quotes by day session to be displayed in a front end application
    """

    def __init__(self):
        db_query_config = QuotesByDaySessionDbQueryConfig()
        query_param_cast_map: Dict[str, str] = {
            'trade_date': 'date',
            'update_time': 'time',
            'product_code': 'text',
        }
        super().__init__(config=db_query_config, query_param_cast_map=query_param_cast_map)

    @quotes_by_day_session_router.get('/quotes-by-day-session', response_model=MicroserviceListResponse)
    def list(self,
             q: Optional[str] = Query(
                 None,
                 title="SQL Query string",
                 description="A more fluid way to filter using actual SQL queries starting with optional 'WHERE'",
                 example="WHERE trade_date = '2020-12-24'::date"
             ),
             trade_date: Optional[str] = Query(None, description='The trade date in YYYY-MM-DD', example='2020-12-24'),
             update_time: Optional[str] = Query(None, description='The update time in hh:mm:ss', example='16:03:00'),
             product_code: Optional[str] = Query(None, description='The product code for the trade',
                                                 example='CRUDE OIL'),
             skip: Optional[int] = Query(0, ge=0),
             limit: Optional[int] = Query(
                 microservice_config.default_pagination_limit,
                 le=microservice_config.maximum_pagination_limit)
             ):
        q_from_params = self.generate_q_param_from_params(
            trade_date=trade_date, update_time=update_time, product_code=product_code).strip()

        if q is None and q_from_params != '':
            q = q_from_params
        elif isinstance(q, str) and q_from_params != '':
            q = f'{q} AND {q_from_params}'

        result = self._list(limit=limit, offset=skip, q=q, should_fetch_total=True)
        return dict(data=result.data, total=result.total, skip=skip, limit=limit)

    def get_one(self, *args, **kwargs):
        pass

    @quotes_by_day_session_router.websocket('/quotes-by-day-session')
    async def websocket_list(self, websocket: WebSocket,
                             q: Optional[str] = Query(None),
                             trade_date: Optional[str] = Query(None),
                             update_time: Optional[str] = Query(None),
                             product_code: Optional[str] = Query(None),
                             skip: Optional[int] = Query(0, ge=0),
                             limit: Optional[int] = Query(
                                 microservice_config.default_pagination_limit,
                                 le=microservice_config.maximum_pagination_limit
                             )):
        """Sends list data via the websocket medium"""
        await super().websocket_list(websocket=websocket, response_model=MicroserviceListResponse,
                                     q=q, limit=limit, skip=skip, trade_date=trade_date,
                                     update_time=update_time, product_code=product_code)

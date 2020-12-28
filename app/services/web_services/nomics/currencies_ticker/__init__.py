"""
Module containing the currencies_ticker microservice
"""
from typing import Optional, List, Dict, Any

from app.abstract.services.web_service.config import MicroserviceConfig, MicroserviceListResponse
from app.abstract.services.web_service.readonly_microservice import ReadOnlyMicroservice
from fastapi import APIRouter, Query, WebSocket
from fastapi_utils.cbv import cbv

from .config import NomicsCurrenciesTickerDbQueryConfig

currencies_ticker_router = APIRouter()
microservice_config = MicroserviceConfig()


@cbv(currencies_ticker_router)
class CurrenciesTickerMicroservice(ReadOnlyMicroservice):
    """
    Returns data for almost realtime price of the digital currencies to be displayed in a front end application
    """

    def __init__(self):
        db_query_config = NomicsCurrenciesTickerDbQueryConfig()
        query_param_cast_map: Dict[str, str] = {
            'price_date': 'date',
            'currency': 'text'
        }
        super().__init__(config=db_query_config, query_param_cast_map=query_param_cast_map)

    @currencies_ticker_router.get('/currencies-ticker', response_model=MicroserviceListResponse)
    def list(self,
             q: Optional[str] = Query(
                 None,
                 title="SQL Query string",
                 description="A more fluid way to filter using actual SQL queries starting with optional 'WHERE'",
                 example="WHERE price_date = '2020-12-24'::date and id = 'ETH'"
             ),
             currency: Optional[str] = Query(None, description='The id of the currency e.g. BTC for bitcoin',
                                             example='BTC'),
             price_date: Optional[str] = Query(None, description='The price date as string YYYY-MM-DD e.g. 2020-12-24',
                                               example='2020-12-24'),
             skip: Optional[int] = Query(0, ge=0),
             limit: Optional[int] = Query(
                 microservice_config.default_pagination_limit,
                 le=microservice_config.maximum_pagination_limit)
             ):
        q_from_params = self.generate_q_param_from_params(price_date=price_date, currency=currency).strip()

        if q is None and q_from_params != '':
            q = q_from_params
        elif isinstance(q, str) and q_from_params != '':
            q = f'{q} AND {q_from_params}'

        result = self._list(limit=limit, offset=skip, q=q, should_fetch_total=True)
        return dict(data=result.data, total=result.total, skip=skip, limit=limit)

    def get_one(self, *args, **kwargs):
        pass

    @currencies_ticker_router.websocket('/currencies-ticker')
    async def websocket_list(self, websocket: WebSocket,
                             q: Optional[str] = Query(None),
                             currency: Optional[str] = Query(None),
                             price_date: Optional[str] = Query(None),
                             skip: Optional[int] = Query(0, ge=0),
                             limit: Optional[int] = Query(
                                 microservice_config.default_pagination_limit,
                                 le=microservice_config.maximum_pagination_limit
                             )):
        """Sends list data via the websocket medium"""
        await super().websocket_list(websocket=websocket, response_model=MicroserviceListResponse,
                                     q=q, limit=limit, skip=skip, price_date=price_date, currency=currency)

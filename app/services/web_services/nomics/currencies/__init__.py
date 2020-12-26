"""
Module containing the currencies microservice
"""
from typing import Optional

from app.abstract.services.web_service.config import MicroserviceConfig, MicroserviceListResponse
from app.abstract.services.web_service.readonly_microservice import ReadOnlyMicroservice
from fastapi import APIRouter, Query, WebSocket
from fastapi_utils.cbv import cbv

from app.services.web_services.nomics.currencies.config import NomicsCurrenciesDbQueryConfig

currencies_router = APIRouter()
microservice_config = MicroserviceConfig()


@cbv(currencies_router)
class CurrenciesMicroservice(ReadOnlyMicroservice):
    """
    Returns data for currencies to be displayed in a front end application
    """

    def __init__(self):
        db_query_config = NomicsCurrenciesDbQueryConfig()
        super().__init__(config=db_query_config)

    @currencies_router.get('/currencies', response_model=MicroserviceListResponse)
    def list(self,
             q: Optional[str] = Query(
                 None,
                 title="SQL Query string",
                 description="Filter using actual SQL queries starting with optional 'WHERE'",
                 example="WHERE name ILIKE '10%'"
             ),
             skip: Optional[int] = Query(0, ge=0),
             limit: Optional[int] = Query(
                 microservice_config.default_pagination_limit,
                 le=microservice_config.maximum_pagination_limit)
             ):
        result = self._list(limit=limit, offset=skip, q=q, should_fetch_total=True)
        return dict(data=result.data, total=result.total, skip=skip, limit=limit)

    def get_one(self, *args, **kwargs):
        pass

    @currencies_router.websocket('/currencies')
    async def websocket_list(self, websocket: WebSocket,
                             q: Optional[str] = Query(None),
                             skip: Optional[int] = Query(0, ge=0),
                             limit: Optional[int] = Query(
                                 microservice_config.default_pagination_limit,
                                 le=microservice_config.maximum_pagination_limit
                             )):
        """Sends list data via the websocket medium"""
        await super().websocket_list(websocket=websocket, response_model=MicroserviceListResponse,
                                     q=q, limit=limit, skip=skip)

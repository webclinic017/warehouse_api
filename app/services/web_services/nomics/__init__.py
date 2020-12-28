from app.abstract.services.web_service.config import WebServiceRouterConfig

from .currencies import currencies_router
from .currencies_ticker import currencies_ticker_router

__NOMICS_TAG = 'nomics'

NOMICS_ROUTER_CONFIGS = [
    WebServiceRouterConfig(tag=__NOMICS_TAG, router=currencies_router),
    WebServiceRouterConfig(tag=__NOMICS_TAG, router=currencies_ticker_router),
]

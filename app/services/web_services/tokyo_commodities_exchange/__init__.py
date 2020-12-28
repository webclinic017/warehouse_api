from app.abstract.services.web_service.config import WebServiceRouterConfig

from .quotes_by_day_session import quotes_by_day_session_router
from .quotes_by_night_session import quotes_by_night_session_router

__TOKYO_COMMODITIES_EXCHANGE_TAG = 'tokyo-commodities-exchange'

TOKYO_COMMODITIES_EXCHANGE_ROUTER_CONFIGS = [
    WebServiceRouterConfig(tag=__TOKYO_COMMODITIES_EXCHANGE_TAG, router=quotes_by_day_session_router),
    WebServiceRouterConfig(tag=__TOKYO_COMMODITIES_EXCHANGE_TAG, router=quotes_by_night_session_router),
]

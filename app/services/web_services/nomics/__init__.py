from app.abstract.services.web_service.config import WebServiceRouterConfig

from .currencies import currencies_router

__NOMICS_TAG = 'nomics'

NOMICS_ROUTER_CONFIGS = [
    WebServiceRouterConfig(tag=__NOMICS_TAG, router=currencies_router),
]

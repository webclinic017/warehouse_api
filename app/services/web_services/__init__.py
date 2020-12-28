"""
Holds the function to run all or some of the web services
"""
from typing import List

from .nomics import NOMICS_ROUTER_CONFIGS
from .tokyo_commodities_exchange import TOKYO_COMMODITIES_EXCHANGE_ROUTER_CONFIGS
from ...abstract.services.web_service.config import WebServiceRouterConfig

WEB_SERVICES_ROUTER_CONFIGS: List[WebServiceRouterConfig] = (
        NOMICS_ROUTER_CONFIGS +
        TOKYO_COMMODITIES_EXCHANGE_ROUTER_CONFIGS
)

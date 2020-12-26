"""
Module to run all http services
"""
import uvicorn
from fastapi import FastAPI

from app.abstract.web_servers import configure_rest_server
from app.services.database_services import DB_CONFIGS
from app.services.web_services import WEB_SERVICES_ROUTER_CONFIGS
from app.abstract.services.web_service.config import WebServiceConfig


def run(app: FastAPI):
    """
    Runs the REST web server
    """
    web_service_config = WebServiceConfig()
    configure_rest_server(app=app, router_configs=WEB_SERVICES_ROUTER_CONFIGS, db_configs=DB_CONFIGS)
    uvicorn.run(app=app, host=web_service_config.host, port=int(web_service_config.http_port),)

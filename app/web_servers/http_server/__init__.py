"""
Module to run all http services
"""
import uvicorn
from fastapi import FastAPI

from app.abstract.web_servers import configure_rest_server
from app.services.database_services import DB_CONFIGS
from app.services.web_services import WEB_SERVICES_ROUTER_CONFIGS
from web_config import WebServiceConfig


def create_app():
    """Configures the FastAPI app and returns it"""
    app = FastAPI()
    configure_rest_server(app=app, router_configs=WEB_SERVICES_ROUTER_CONFIGS, db_configs=DB_CONFIGS)
    return app


def run(app: FastAPI, web_service_config: WebServiceConfig = WebServiceConfig()):
    """
    Runs the REST web server in development using uvicorn
    """
    uvicorn.run(app=app, host=web_service_config.host, port=web_service_config.http_port, )

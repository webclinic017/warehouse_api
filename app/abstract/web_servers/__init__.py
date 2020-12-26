"""
Module containing abstract classes for web services
"""
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.abstract.services.database_service.config import DatabaseConnectionConfig
from app.abstract.services.database_service.db_connection import DatabaseConnection
from app.abstract.services.web_service.config import WebServiceRouterConfig


def configure_rest_server(app: FastAPI, router_configs: List[WebServiceRouterConfig],
                          db_configs: List[DatabaseConnectionConfig]):
    """Configures the fast api rest api but does not start uvicorn"""

    @app.on_event('startup')
    def open_database_connections():
        DatabaseConnection.open_connections(db_configs=db_configs)

    @app.on_event('shutdown')
    def close_database_connections():
        DatabaseConnection.close_all_connections()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router_config in router_configs:
        app.include_router(router=router_config.router,
                           prefix=f"/{router_config.tag}",
                           tags=[router_config.tag])


def run_graphql_server(self, *args, **kwargs):
    raise NotImplementedError("run_as_graphql not implemented")

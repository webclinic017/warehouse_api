"""
Configuration file for gunicorn https://docs.gunicorn.org/en/stable/configure.html#configuration-file
It also serves as an initializer for the uvicorn app server in case of running in development
"""

import os

from pydantic import BaseModel
from dotenv import load_dotenv

# load environment variables
load_dotenv()


class WebServiceConfig(BaseModel):
    host: str = os.environ.get('HOST', '0.0.0.0')
    http_port: int = int(os.environ.get('HTTP_PORT', '5400'))
    gunicorn_workers: int = os.environ.get('GUNICORN_WORKERS', '4')
    gunicorn_worker_class: str = 'uvicorn.workers.UvicornWorker'  # to run uvicorn under gunicorn


web_service_config = WebServiceConfig()

bind = f'{web_service_config.host}:{web_service_config.http_port}'
workers = web_service_config.gunicorn_workers
worker_class = web_service_config.gunicorn_worker_class

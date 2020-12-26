"""
Module to hold the basic configuration class for web service
"""
import os
from typing import Any, List
from fastapi import APIRouter

from pydantic import BaseModel


class WebServiceConfig(BaseModel):
    host: str = os.environ.get('HOST', '0.0.0.0')
    http_port: str = os.environ.get('HTTP_PORT', 5400)


class WebServiceRouterConfig(BaseModel):
    tag: str
    router: APIRouter

    class Config:
        arbitrary_types_allowed = True


class MicroserviceConfig(BaseModel):
    default_pagination_limit: int = int(os.environ.get('DEFAULT_PAGINATION_LIMIT', 20))
    maximum_pagination_limit: int = int(os.environ.get('MAXIMUM_PAGINATION_LIMIT', 100))


class MicroserviceListResponse(BaseModel):
    data: List[Any]
    total: int
    skip: int
    limit: int

    class Config:
        orm_mode = True


"""
Module with database services pydantic schema
"""
import os
from typing import Union, List, Dict, Any, Optional
import sqlalchemy.engine as sqlalchemy_engine
from pydantic import BaseModel

_ROW_PROXY = sqlalchemy_engine.RowProxy
MAX_WORKER_THREADS = min(32, os.cpu_count() + 4)
THREAD_NAME_PREFIX = 'WAREHOUSE_API'


class DatabaseConnectionConfig(BaseModel):
    db_uri: str
    pool_size: int = 5
    reflect: bool = True
    autocommit: bool = False
    pool_timeout: int = 60


class DbQueryConfig(BaseModel):
    label: str
    sql: str
    db_config: DatabaseConnectionConfig


class DbQueryReturnType(BaseModel):
    data: Union[_ROW_PROXY, List[Any], Dict[str, Any]] = None
    total: int = None

    class Config:
        arbitrary_types_allowed = True


class DbQueryRunOptions(BaseModel):
    # params for sql query
    params: Optional[Dict[str, Any]] = {}
    limit: Optional[int] = None
    offset: Optional[int] = None
    multiple_records: Optional[bool] = True
    should_fetch_total: Optional[bool] = False
    q: Optional[str] = None

    class Config:
        arbitrary_types_allowed = False

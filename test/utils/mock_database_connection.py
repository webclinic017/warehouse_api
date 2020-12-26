"""Module Holds the mock data connection class"""
import logging
import os
from typing import Optional, Dict, Any

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.sql import text


class MockDatabaseConnection:
    """
    Connects to a given database, returning a session in a context manager, and runs a given query
    """

    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        pool_size: int = 5
        pool_timeout: int = 60
        self.db_session: Optional[Session] = None
        self.connection_engine: engine.Engine = create_engine(
            self.db_uri,
            pool_size=pool_size,
            max_overflow=pool_size + 1,
            pool_timeout=pool_timeout,
        )

    def __enter__(self):
        """
        Creates a scoped session for the database that is thread-safe for reads
        """
        session = sessionmaker(
            bind=self.connection_engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
        self.db_session = scoped_session(session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        This runs at the end of the 'with' statement as a way of cleaning up
        """
        self.db_session.commit()
        self.db_session.close()

    def close(self):
        """
        Closes the db connection engine
        """
        try:
            self.connection_engine.dispose()
            logging.info(f'Successfully closed connection {self.db_uri}')
        except Exception as exp:
            logging.warning(str(exp))

    def execute_sql(self, sql: str, params: Dict[str, Any] = {}) -> engine.ResultProxy:
        """
        Executes the sql passed as a parameter
        """
        return self.db_session.execute(text(sql), params=params)

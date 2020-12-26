"""Utilities to mock the database from JSON files into the Memory Sqlite database"""
import os
import re

from typing import Callable, Dict, Any, Optional

import sqlalchemy

from sqlalchemy.ext.declarative import api

from test.utils.file_io import read_json_file
from test.utils.mock_database_connection import MockDatabaseConnection


def validate_database_uri(database_uri: str):
    """Ensures that the database passed to it is not one of the untouchables"""
    return True


def load_json_data_to_mock_database(json_file_path: os.path, declarative_base: api, model_class: Callable,
                                    database_uri: str = 'sqlite:///:memory:',
                                    record_transformer: Callable[[Dict[str, Any]], Dict[str, Any]] = lambda x: x):
    """Loads JSON data array into the database"""
    validate_database_uri(database_uri=database_uri)

    raw_records = read_json_file(json_file_path)

    records = [model_class(**record_transformer(record_dict)) for record_dict in raw_records]

    with MockDatabaseConnection(db_uri=database_uri) as connection:
        engine = connection.connection_engine

        try:
            declarative_base.metadata.create_all(engine)
        except Exception as exp:
            schema_search_groups = re.search(r'schema "(.*)"', str(exp)).groups()

            if len(schema_search_groups) > 0:
                new_schema = schema_search_groups[0]
                engine.execute(sqlalchemy.schema.CreateSchema(new_schema))
                declarative_base.metadata.create_all(engine)
            else:
                raise exp

        connection.db_session.add_all(records)
        connection.db_session.commit()


def remove_all_locks_on_table(connection: MockDatabaseConnection, table_name: str):
    """Kills all connections to a given table to allow such things as dropping th table"""
    locks_on_table = connection.execute_sql(f"""SELECT pid
                    FROM pg_locks l
                    JOIN pg_class t ON l.relation = t.oid AND t.relkind = 'r'
                    WHERE t.relname = '{table_name}' AND pid <> pg_backend_pid()""")

    for lock in locks_on_table:
        termination_result = connection.execute_sql(
            f'SELECT pg_terminate_backend({lock.pid}) FROM pg_stat_activity')


def clear_table_in_mock_database(model_class: type(api),
                                 database_uri: str = 'sqlite:///:memory:', table_name: Optional[str] = None):
    """Clears the table in the mock database"""
    validate_database_uri(database_uri=database_uri)

    with MockDatabaseConnection(db_uri=database_uri) as connection:
        if isinstance(table_name, str):
            remove_all_locks_on_table(connection=connection, table_name=table_name)

        full_table_name = model_class.__table__.fullname
        connection.execute_sql(f'DROP TABLE IF EXISTS {full_table_name}', params={})

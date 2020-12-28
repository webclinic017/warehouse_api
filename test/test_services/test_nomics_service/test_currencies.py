"""Test for nomics/currencies microservice"""
import os
import unittest

from fastapi import FastAPI

from dotenv import load_dotenv

try:
    load_dotenv(
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.local.env'))
finally:
    pass

from test.utils.base_test_for_microservices import TestCase
from test.utils.config import RawDatabaseMockAsset
from test.utils.mock_models import Currencies


class TestCurrenciesMicroservice(TestCase):
    """Tests for the nomics currencies microservice"""
    app = FastAPI()
    url_path = '/nomics/currencies'
    raw_database_mock_assets = [
        RawDatabaseMockAsset(
            db_uri=os.getenv('NOMICS_LIVE_DB_URI'),
            db_name='nomics_live_db',
            db_table_name='currencies',
            model_class=Currencies)]
    service_name = 'nomics'
    microservice_name = 'currencies'


if __name__ == '__main__':
    unittest.main()

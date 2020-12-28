"""Test for nomics/currencies_ticker microservice"""
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
from test.utils.mock_models import CurrenciesTicker


class TestCurrenciesTickerMicroservice(TestCase):
    """Tests for the nomics currencies_ticker microservice"""
    app = FastAPI()
    url_path = '/nomics/currencies-ticker'
    raw_database_mock_assets = [
        RawDatabaseMockAsset(
            db_uri=os.getenv('NOMICS_LIVE_DB_URI'),
            db_name='nomics_live_db',
            db_table_name='currencies_ticker',
            model_class=CurrenciesTicker)]
    service_name = 'nomics'
    microservice_name = 'currencies_ticker'


if __name__ == '__main__':
    unittest.main()

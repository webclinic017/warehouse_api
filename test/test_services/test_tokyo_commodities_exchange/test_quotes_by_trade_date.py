"""Test for tokyo-commodities-exchange/quotes-by-trade-date microservice"""
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
from test.utils.mock_models import QuotesByTradeDate


class TestQuotesByTradeDateMicroservice(TestCase):
    """Tests for the Tokyo Commodities Exchanges quotes by trade date microservice"""
    app = FastAPI()
    url_path = '/tokyo-commodities-exchange/quotes-by-trade-date'
    raw_database_mock_assets = [
        RawDatabaseMockAsset(
            db_uri=os.getenv('TOKYO_COMMODITIES_HISTORICAL_DB_URI'),
            db_name='tokyo_commodities_historical',
            db_table_name='quotes_by_trade_date',
            model_class=QuotesByTradeDate)]
    service_name = 'tokyo_commodities_exchange'
    microservice_name = 'quotes_by_trade_date'


if __name__ == '__main__':
    unittest.main()

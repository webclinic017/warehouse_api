"""Base Class for all tests on Web microservices"""
import json
import unittest
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Union, Optional

from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.abstract.services.web_service.config import MicroserviceConfig
from app.services.database_services import DB_CONFIGS
from app.services.web_services import WEB_SERVICES_ROUTER_CONFIGS
from test.utils.config import RawDatabaseMockAsset, IntermediateResponseMockAsset, FinalResponseMockAsset

from app.abstract.web_servers import configure_rest_server

microservice_config = MicroserviceConfig()


class TestCase(unittest.TestCase):
    """Tests for web microservice"""
    app: FastAPI
    page_limit: int = microservice_config.maximum_pagination_limit
    __maximum_limit: int = microservice_config.maximum_pagination_limit
    service_name: str  # e.g. nomics_service
    microservice_name: str  # e.g. currencies
    url_path: str  # e.g. nomics/currencies
    raw_database_mock_assets: List[RawDatabaseMockAsset] = []
    intermediate_response_mock_assets: Dict[str, IntermediateResponseMockAsset] = {}
    final_response_mock_asset: FinalResponseMockAsset = None

    @classmethod
    def process_expected_data_record(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        """Modifies the expected data record accordingly"""
        return record

    @classmethod
    def process_snapshot_data_record(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        """Modifies the snapshot data record before it is saved to the expected folder"""
        return record

    @classmethod
    def process_intermediate_data(cls, mock_assets: Dict[str, IntermediateResponseMockAsset]) -> Union[
        List[Dict[str, Any]], Dict[str, Any]]:
        """Modifies the intermediate data assets to return a single response"""
        if len(cls.intermediate_response_mock_assets) > 0:
            raise NotImplementedError(
                'process_intermediate_data should be implemented if intermediate responses are available')
        return []

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize the database assets
        configure the fast api app
        """
        for raw_database_mock_asset in cls.raw_database_mock_assets:
            raw_database_mock_asset.load_asset()

        if hasattr(cls, 'app'):
            configure_rest_server(app=cls.app, router_configs=WEB_SERVICES_ROUTER_CONFIGS, db_configs=DB_CONFIGS)

            cls.final_response_mock_asset = FinalResponseMockAsset(service_name=cls.service_name,
                                                                   name=f"{cls.microservice_name}_list")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Delete records in database
        """
        for raw_database_mock_asset in cls.raw_database_mock_assets:
            raw_database_mock_asset.clear_asset()

    def setUp(self) -> None:
        """Initialize a few things"""
        self.client: Optional[TestClient] = None

        if hasattr(self, 'app'):
            self.client = TestClient(app=self.app)

    def _test_final_list_response(self, response: Dict[str, Any]):
        """Tests the response returned in a list view"""
        try:
            expected_response = self.final_response_mock_asset.load_asset(
                record_transformer=self.process_expected_data_record)
            limit = min(self.page_limit, self.__maximum_limit)

            self.assertGreaterEqual(response['total'], len(expected_response))
            self.assertEqual(response['skip'], 0)
            self.assertEqual(response['limit'], limit)
            self.assertListEqual(response['data'], expected_response[:limit])
        except FileNotFoundError:
            # Save the snapshot
            self.final_response_mock_asset.dump_asset(response['data'],
                                                      snapshot_transformer=self.process_snapshot_data_record)

    def test_expected_response_list(self):
        """
        Should return the expected data in the expected_data folder
        """
        if isinstance(self.client, TestClient):
            response = self.client.get(self.url_path, params=dict(limit=self.page_limit))
            self.assertEqual(response.status_code, 200)
            response_json = response.json()
            self._test_final_list_response(response=response_json)

    def test_expected_response_websocket_list(self):
        """
        Should return the expected data in the expected_data folder
        """
        if isinstance(self.client, TestClient):
            with self.client.websocket_connect(f'{self.url_path}?limit={self.page_limit}') as websocket:
                websocket_response = websocket.receive_json()
            response = json.loads(websocket_response)
            self._test_final_list_response(response=response)

    def test_intermediate_response_list(self):
        """
        Should return the data that is equal to that computed from intermediate assets
        """
        if hasattr(self, 'app') and len(self.intermediate_response_mock_assets) > 0:
            response = self.client.get(self.url_path, params=dict(limit=self.page_limit))
            self.assertEqual(response.status_code, 200)

            response_json = response.json()

            expected_response = self.process_intermediate_data(mock_assets=self.intermediate_response_mock_assets)
            limit = min(self.page_limit, self.__maximum_limit)

            self.assertGreaterEqual(response_json['total'], len(expected_response))
            self.assertEqual(response_json['skip'], 0)
            self.assertEqual(response_json['limit'], limit)
            self.assertListEqual(response_json['data'], expected_response[:limit])

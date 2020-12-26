"""Module contains the config classes for the test cases"""
from datetime import timedelta, date
from typing import Optional, Callable, Any, List, Dict, Union

from pydantic import BaseModel

from test.utils.file_io import get_file_path_from_mocks_folder, read_json_file, write_to_json_file
from test.utils.mock_database import clear_table_in_mock_database, load_json_data_to_mock_database
from test.utils.mock_models import Base


class RawDatabaseMockAsset(BaseModel):
    """The class to hold assets for the mock database assets"""
    db_uri: str = "postgres://postgres:password123@localhost:5432/test_warehouse_api?application_name=warehouse_api"
    db_name: str  # e.g. nomics_live
    db_table_name: str  # e.g. currencies
    model_class: type(Base)  # e.g. Currencies
    mock_subdirectory: str = 'raw_data'
    should_delete_old_data: bool = True

    @staticmethod
    def record_transformer(value):
        return value

    class Config:
        arbitrary_types_allowed = True

    def load_asset(self):
        """Loads the asset into the database"""
        if self.should_delete_old_data:
            try:
                clear_table_in_mock_database(model_class=self.model_class, database_uri=self.db_uri,
                                             table_name=self.db_table_name)
            finally:
                pass
        raw_data_json_path = get_file_path_from_mocks_folder(self.mock_subdirectory, self.db_name,
                                                             f'{self.db_table_name}.json')
        load_json_data_to_mock_database(json_file_path=raw_data_json_path, declarative_base=Base,
                                        model_class=self.model_class, database_uri=self.db_uri,
                                        record_transformer=self.record_transformer)

    def clear_asset(self):
        """Clears the asset in the database"""
        clear_table_in_mock_database(model_class=self.model_class, database_uri=self.db_uri,
                                     table_name=self.db_table_name)


class RawDatabaseMockAssetForDayAhead(RawDatabaseMockAsset):
    """This asset deals with data that is for day ahead values i.e. values in future"""
    days_ahead: int = 1
    date_field: str

    def record_transformer(self, value: Dict[str, Any]):
        new_value = value.copy()
        new_value[self.date_field] = date.today() + timedelta(days=self.days_ahead)
        return new_value


class ResponseMockAsset(BaseModel):
    """The class to hold assets that are either intermediate or final responses"""
    service_name: str  # e.g. nomics
    mock_subdirectory: str  # 'intermediate_data' for intermediate, expected_data for final responses
    name: str  # for final responses, this is the microservice name

    def load_asset(self, record_transformer: Callable[[Dict[str, Any]], Dict[str, Any]] = lambda x: x) -> Union[
        List[Dict[str, Any]], Dict[str, Any]]:
        """Returns the mock asset as a list or dictionary"""
        file_path = get_file_path_from_mocks_folder(self.mock_subdirectory, self.service_name,
                                                    f'{self.name}.json')
        return read_json_file(file_path, pre_populator=record_transformer)


class IntermediateResponseMockAsset(ResponseMockAsset):
    """The class to hold an intermediate response asset"""
    mock_subdirectory: str = 'intermediate_data'


class FinalResponseMockAsset(ResponseMockAsset):
    """The class to hold a final response asset"""
    mock_subdirectory: str = 'expected_data'

    def dump_asset(self, data: Union[List[Dict[str, Any]], Dict[str, Any]],
                   snapshot_transformer: Callable[[Dict[str, Any]], Dict[str, Any]] = lambda x: x):
        """Returns the mock asset as a list or dictionary"""
        file_path = get_file_path_from_mocks_folder(self.mock_subdirectory, self.service_name,
                                                    f'{self.name}.json')
        return write_to_json_file(file_path, data=data, pre_populator=snapshot_transformer)

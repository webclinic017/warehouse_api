"""Module for input out of json files"""

import json
import os
from typing import Any, Dict, Callable, Optional, Union, List

_MOCKS_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'mocks')


def read_json_file(json_file_path: os.path, pre_populator: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
    """Returns the data that was in the JSON file as a python object"""
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    if callable(pre_populator):
        if isinstance(data, Dict):
            return pre_populator(data)
        elif isinstance(data, list):
            return [pre_populator(record) for record in data]

    return data


def write_to_json_file(json_file_path: os.path, data: Union[List[Dict[str, Any]], Dict[str, Any]], pre_populator: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
    """Writes the data to a JSON file"""
    processed_data = data.copy()

    if callable(pre_populator):
        if isinstance(data, Dict):
            processed_data = pre_populator(data)
        elif isinstance(data, list):
            processed_data = [pre_populator(record) for record in data]

    with open(json_file_path, 'w') as json_file:
        json.dump(processed_data, json_file)


def get_file_path_from_mocks_folder(*path_fragments):
    """
    Returns a file path for a given sequence of arguments,
    starting at the root of the mocks folder
    """
    return os.path.join(_MOCKS_DIRECTORY, *path_fragments)

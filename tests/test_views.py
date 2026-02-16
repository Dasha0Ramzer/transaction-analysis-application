import json
import os
from typing import Any
from unittest.mock import mock_open, patch

from src.views import events_page_json, home_page_json, service_profitable_categories_of_increased_cashback_json


@patch("builtins.open", new_callable=mock_open)
def test_home_page_json(mock_file: Any) -> None:
    test_data = {"message": "Привет, мир!"}
    home_page_json(test_data)
    data_directory_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    root_directory_ = os.path.join(data_directory_, "home_page.json")
    mock_file.assert_called_once_with(root_directory_, "w", encoding="utf-8")
    handle = mock_file()
    written_data = "".join(call[0][0] for call in handle.write.call_args_list)
    assert json.loads(written_data) == test_data


@patch("builtins.open", new_callable=mock_open)
def test_events_page_json(mock_file: Any) -> None:
    test_data = {"message": "Привет, мир!"}
    events_page_json(test_data)
    data_directory_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    root_directory_ = os.path.join(data_directory_, "events_page.json")
    mock_file.assert_called_once_with(root_directory_, "w", encoding="utf-8")
    handle = mock_file()
    written_data = "".join(call[0][0] for call in handle.write.call_args_list)
    assert json.loads(written_data) == test_data


@patch("builtins.open", new_callable=mock_open)
def test_service_profitable_categories_of_increased_cashback_json(mock_file: Any) -> None:
    test_data = {"message": "Привет, мир!"}
    service_profitable_categories_of_increased_cashback_json(test_data)
    data_directory_ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    root_directory_ = os.path.join(data_directory_, "profitable_categories_of_increased_cashback.json")
    mock_file.assert_called_once_with(root_directory_, "w", encoding="utf-8")
    handle = mock_file()
    written_data = "".join(call[0][0] for call in handle.write.call_args_list)
    assert json.loads(written_data) == test_data

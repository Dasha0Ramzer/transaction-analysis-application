import datetime
from typing import Any, Hashable
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (cards, cashback, exchange_rate, filtering_by_date, greeting, stock_price, top_transactions,
                       total_expenses, xlsx_file_reader)


@pytest.mark.parametrize(
    "date_time_now, expected",
    [
        (datetime.datetime(2023, 10, 1, 3, 0), "Доброй ночи"),
        (datetime.datetime(2026, 2, 10, 6, 0), "Доброе утро"),
        (datetime.datetime(2026, 2, 10, 14, 0), "Добрый день"),
        (datetime.datetime(2026, 2, 10, 19, 0), "Добрый вечер"),
    ],
)
def test_greeting(date_time_now: datetime.datetime, expected: str) -> None:
    assert greeting(date_time_now) == expected


excel_content = pd.DataFrame({"ID": [650703], "State": ["EXECUTED"]})


@patch("pandas.read_excel")
def test_xlsx_file_reader(mock_read_excel: Any) -> None:
    mock_read_excel.return_value = excel_content
    result = xlsx_file_reader("path_to_the_file")
    expected = [
        {
            "ID": 650703,
            "State": "EXECUTED",
        }
    ]
    assert result == expected


@pytest.mark.parametrize(
    "date_time_now, expected",
    [
        (
            datetime.datetime(2021, 12, 5, 3, 0),
            [
                {
                    "Дата операции": "02.12.2021 16:44:00",
                    "Номер карты": "*2345",
                    "Сумма платежа": -13,
                    "Категория": "покупка",
                    "Описание": "пятерочка",
                },
                {
                    "Дата операции": "01.12.2021 16:44:00",
                    "Номер карты": "*1234",
                    "Сумма платежа": -14,
                    "Категория": "покупка",
                    "Описание": "пятерочка",
                },
            ],
        )
    ],
)
def test_filtering_by_date(
    data_fixture: list[dict[Hashable, Any]], date_time_now: datetime.datetime, expected: list[dict[str, Any]]
) -> None:
    assert filtering_by_date(data_fixture, date_time_now) == expected


def test_cards(data_fixture: list[dict[Hashable, Any]]) -> None:
    generator = cards(data_fixture)
    assert next(generator) == "*4567"
    assert next(generator) == "*3456"
    assert next(generator) == "*1234"
    assert next(generator) == "*2345"


def test_total_expenses(data_fixture: list[dict[Hashable, Any]]) -> None:
    assert total_expenses(data_fixture, ["*1234", "*3456", "*2345"]) == {"*1234": 26, "*2345": 13}


def test_cashback() -> None:
    assert cashback(1234.56) == 12.35


def test_top_transactions(data_fixture: list[dict[Hashable, Any]]) -> None:
    assert top_transactions(data_fixture) == [
        {
            "date": "31.12.2021",
            "amount": -10,
            "category": "покупка",
            "description": "пятерочка",
        },
        {
            "date": "15.12.2021",
            "amount": 11,
            "category": "пополнение",
            "description": "банкомат",
        },
        {
            "date": "10.12.2021",
            "amount": -12,
            "category": "покупка",
            "description": "пятерочка",
        },
        {
            "date": "02.12.2021",
            "amount": -13,
            "category": "покупка",
            "description": "пятерочка",
        },
        {
            "date": "01.12.2021",
            "amount": -14,
            "category": "покупка",
            "description": "пятерочка",
        },
    ]


@patch("builtins.open", new_callable=mock_open)
@patch("requests.get")
def test_exchange_rate(
    mock_get: Any, mock_open: Any, fake_user_settings: str, fake_api_response_1: dict[str, Any]
) -> None:
    mock_open.return_value.read.return_value = fake_user_settings
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_api_response_1
    result = exchange_rate()
    assert len(result) == 1
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 75.0


@patch("builtins.open", new_callable=mock_open)
@patch("requests.get")
def test_stock_price(
    mock_get: Any, mock_open: Any, fake_user_settings: str, fake_api_response_2: dict[str, Any]
) -> None:
    mock_open.return_value.read.return_value = fake_user_settings
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_api_response_2
    result = stock_price()
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 75.0

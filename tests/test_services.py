import json
from typing import Any, Hashable

import pytest

from src.services import (investment_bank, profitable_categories_of_increased_cashback, search_by_phone_numbers,
                          search_for_transfers_to_individuals, simple_search)


@pytest.mark.parametrize(
    "year, month, expected",
    [(2021, 2, {"Ж/д билеты": 58.0}), (2021, 12, {})],
)
def test_profitable_categories_of_increased_cashback(
    data_fixture_2: list[dict[Hashable, Any]], year: int, month: int, expected: dict[str, float]
) -> None:
    expected_json = json.dumps(expected, indent=4)
    assert profitable_categories_of_increased_cashback(data_fixture_2, year, month) == expected_json


@pytest.mark.parametrize(
    "month, limit, expected",
    [("2021-02", 10, 14.48), ("2021-12", 50, 0)],
)
def test_investment_bank(data_fixture_1: list[dict[str, Any]], month: str, limit: int, expected: float) -> None:
    assert investment_bank(month, data_fixture_1, limit) == expected


def test_simple_search(data_fixture_2: list[dict[Hashable, Any]]) -> None:
    expected_json = json.dumps(
        [
            {
                "Дата операции": "12.03.2021 12:27:32",
                "Дата платежа": "12.03.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -278.52,
                "Валюта операции": "RUB",
                "Сумма платежа": -278.52,
                "Валюта платежа": "RUB",
                "Кэшбэк": None,
                "Категория": "Оплата мобильной связи",
                "MCC": 5411.0,
                "Описание": "Мегафон +7 123 45-67-89",
                "Бонусы (включая кэшбэк)": 5,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 278.52,
            }
        ],
        indent=4,
    )
    assert simple_search("Мегафон", data_fixture_2) == expected_json


def test_search_by_phone_numbers(data_fixture_2: list[dict[Hashable, Any]]) -> None:
    expected_json = json.dumps(
        [
            {
                "Дата операции": "12.03.2021 12:27:32",
                "Дата платежа": "12.03.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -278.52,
                "Валюта операции": "RUB",
                "Сумма платежа": -278.52,
                "Валюта платежа": "RUB",
                "Кэшбэк": None,
                "Категория": "Оплата мобильной связи",
                "MCC": 5411.0,
                "Описание": "Мегафон +7 123 45-67-89",
                "Бонусы (включая кэшбэк)": 5,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 278.52,
            }
        ],
        indent=4,
    )
    assert search_by_phone_numbers(data_fixture_2) == expected_json


def test_search_for_transfers_to_individuals(data_fixture_2: list[dict[Hashable, Any]]) -> None:
    expected_json = json.dumps(
        [
            {
                "Дата операции": "10.02.2021 18:19:53",
                "Дата платежа": "10.02.2021",
                "Номер карты": None,
                "Статус": "OK",
                "Сумма операции": -85000.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -85000.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": None,
                "Категория": "Переводы",
                "MCC": None,
                "Описание": "Николай Н.",
                "Бонусы (включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 85000.0,
            }
        ],
        indent=4,
    )
    assert search_for_transfers_to_individuals(data_fixture_2) == expected_json

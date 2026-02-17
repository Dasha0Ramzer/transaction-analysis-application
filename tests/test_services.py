import json
from typing import Any, Hashable

import pytest

from src.services import investment_bank, profitable_categories_of_increased_cashback


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

from typing import Any, Hashable

import pytest

from src.services import profitable_categories_of_increased_cashback


@pytest.mark.parametrize(
    "year, month, expected",
    [(2021, 2, {"Ж/д билеты": 58.0}), (2021, 12, {})],
)
def test_profitable_categories_of_increased_cashback(
    data_fixture_2: list[dict[Hashable, Any]], year: int, month: int, expected: dict[str, float]
) -> None:
    assert profitable_categories_of_increased_cashback(data_fixture_2, year, month) == expected

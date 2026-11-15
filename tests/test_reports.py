from datetime import datetime

import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


def test_spending_by_category(data_fixture_df: pd.DataFrame) -> None:
    result = spending_by_category(data_fixture_df, "еда", "01.04.2023 00:00:00")
    expected_data = pd.DataFrame(
        {
            "Категория": ["еда", "еда"],
            "Дата операции": [datetime(2023, 1, 15, 10, 0), datetime(2023, 3, 5, 14, 0)],
            "Сумма операции": [-100, -75],
        }
    )
    result = result.reset_index(drop=True)
    expected_data = expected_data.reset_index(drop=True)
    assert result.equals(expected_data)


def test_spending_by_weekday(data_fixture_df: pd.DataFrame) -> None:
    result = spending_by_weekday(data_fixture_df, "01.04.2023 00:00:00")
    expected_data = pd.DataFrame(
        {
            "День недели": ["Sunday", "Wednesday"],
            "Сумма операции": [87.5, 200],
        }
    )
    result = result.reset_index(drop=True)
    expected_data = expected_data.reset_index(drop=True)
    assert result.equals(expected_data)


def test_spending_by_workday(data_fixture_df: pd.DataFrame) -> None:
    result = spending_by_workday(data_fixture_df, "01.04.2023 00:00:00")
    expected_data = pd.DataFrame(
        {
            "Тип дня": ["Выходной", "Рабочий"],
            "Сумма операции": [87.5, 200],
        }
    )
    result = result.reset_index(drop=True)
    expected_data = expected_data.reset_index(drop=True)
    assert result.equals(expected_data)

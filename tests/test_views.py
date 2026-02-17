import json

from src.views import create_json_data_events_page, create_json_data_home_page


def test_create_json_data_home_page() -> None:
    test_datetime_str = "2023-01-01 00:00:00"
    expected_result = {
        "greeting": "Доброй ночи",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": [],
    }
    json_result = create_json_data_home_page(test_datetime_str)
    actual_result = json.loads(json_result)
    assert actual_result == expected_result


def test_create_json_data_events_page() -> None:
    test_datetime_str = "2023-01-01 00:00:00"
    expected_result = {
        "expenses": {
            "total_amount": 0,
            "main": [],
            "transfers_and_cash": [],
        },
        "income": {
            "total_amount": 0,
            "main": [],
        },
        "currency_rates": [],
        "stock_prices": [],
    }
    json_result = create_json_data_events_page(test_datetime_str)
    actual_result = json.loads(json_result)
    assert actual_result == expected_result

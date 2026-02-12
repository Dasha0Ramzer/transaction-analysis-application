"""
Основные функции для генерации JSON-ответов
"""
import os
import datetime
import json
import logging
from typing import Any

from src.utils import (cards, cashback, exchange_rate, filtering_by_date, greeting, stock_price, top_transactions,
                       total_expenses, xlsx_file_reader)

views_logger = logging.getLogger("Основные функции для генерации JSON-ответов")

logs_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
views_handler = logging.FileHandler(os.path.join(logs_directory, 'views.log'), mode="w", encoding="utf-8")

views_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - Имя файла: %(filename)s - Имя функции: %(funcName)s \n%(levelname)s - %(message)s"
)
views_handler.setFormatter(views_formatter)
views_logger.addHandler(views_handler)
views_logger.setLevel(logging.DEBUG)


# file_path = "../data/operations.xlsx"
# date_time_now = datetime.datetime.now()
# date_time_now = datetime.datetime(2021, 2, 12, 15, 45, 0)


def create_json_data(path_file: str, datetime_now: datetime.datetime) -> dict[str, Any]:
    """
    Функция, "собирающая" все вспомогательные функции для вывода данных для веб-страницы "Главная"
    :param path_file: путь к файлу с транзакциями
    :type path_file: str
    :param datetime_now: дата и время
    :type datetime_now: datetime.datetime
    :return: JSON-ответ
    :rtype: dict[str, Any]
    """
    views_logger.debug("Собираем вместе все функции из utils.py")
    data_file = xlsx_file_reader(path_file)
    data_filtering_by_date = filtering_by_date(data_file, datetime_now)
    all_cards = list(set(cards(data_filtering_by_date)))
    month_total_expenses = total_expenses(data_filtering_by_date, all_cards)

    views_logger.debug("Формируем данные по каждой карте: последние 4 цифры, сумма трат, кэшбэк")
    card_information = []
    for card_number, summ in month_total_expenses.items():
        card_information.append({"last_digits": card_number[1:], "total_spent": summ, "cashback": cashback(summ)})

    views_logger.debug('Формируем JSON-ответ для веб-страницы "Главная" в соответствии с ТЗ')
    data = {
        "greeting": greeting(datetime_now),
        "cards": card_information,
        "top_transactions": top_transactions(data_filtering_by_date),
        "currency_rates": exchange_rate(),
        "stock_prices": stock_price(),
    }
    return data


def home_page_json(data: Any) -> None:
    """
    Функция, записывающая JSON-ответ в файл для страницы "Главная"
    :return:
    """
    views_logger.debug("Записываем JSON-ответ в файл")
    data_directory_ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    root_directory_ = os.path.join(data_directory_, 'home_page.json')
    with open(root_directory_, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
# root_directory = os.path.join(data_directory, 'operations.xlsx')
# home_page_json(create_json_data(root_directory, datetime.datetime(2021, 2, 12, 15, 45, 0)))

# home_page_json(create_json_data(os.path.join(os.path.dirname(__file__), 'data', 'operations.xlsx'), datetime.datetime(2021, 2, 12, 15, 45, 0)))

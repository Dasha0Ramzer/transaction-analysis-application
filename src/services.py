import datetime
import json
import logging
import os
from typing import Any, Hashable

services_logger = logging.getLogger("Основные функции для генерации JSON-ответов")

logs_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
services_handler = logging.FileHandler(os.path.join(logs_directory, "services.log"), mode="w", encoding="utf-8")

services_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - Имя файла: %(filename)s - Имя функции: %(funcName)s \n%(levelname)s - %(message)s"
)
services_handler.setFormatter(services_formatter)
services_logger.addHandler(services_handler)
services_logger.setLevel(logging.DEBUG)


def profitable_categories_of_increased_cashback(data: list[dict[Hashable, Any]], year: int, month: int) -> str:
    """
    Функция, возвращающая выгодные категории повышенного кэшбэка
    :param data: список операций
    :type data: list[dict[Hashable, Any]]
    :param year: год для анализа
    :type year: int
    :param month: месяц для анализа
    :type month: int
    :return: словарь, где ключ - категория кэшбэка, значение - сумма кэшбэка
    :rtype: dict[str, float]
    """
    start_date = datetime.datetime(year, month, 1, 0, 0, 0)
    if month == 12:
        end_date = datetime.datetime(year + 1, 1, 1, 23, 59, 59) - datetime.timedelta(days=1)
    else:
        end_date = datetime.datetime(year, month + 1, 1, 23, 59, 59) - datetime.timedelta(days=1)
    services_logger.debug(f"Вычисляем начальную ({start_date}) и конечную ({end_date}) даты")

    services_logger.debug("Сортируем операции по дате")
    data_filter_by_period = [
        dict_
        for dict_ in data
        if start_date <= datetime.datetime.strptime(dict_["Дата операции"], "%d.%m.%Y %H:%M:%S") <= end_date
    ]

    services_logger.debug("Суммируем кэшбэк по каждой категории трат")
    categories_of_increased_cashback = {}
    for dict_ in data_filter_by_period:
        if not dict_["Категория"] in categories_of_increased_cashback and dict_["Кэшбэк"] and dict_["Кэшбэк"] > 0:
            categories_of_increased_cashback[dict_["Категория"]] = dict_["Кэшбэк"]
        elif dict_["Категория"] in categories_of_increased_cashback and dict_["Кэшбэк"] > 0:
            categories_of_increased_cashback[dict_["Категория"]] += dict_["Кэшбэк"]

    services_logger.debug("Переводим результат в JSON-формат")
    json_result = json.dumps(categories_of_increased_cashback, indent=4)

    services_logger.info("Возвращаем результат функции")
    return json_result


# from src.utils import xlsx_file_reader
# data_file = xlsx_file_reader('../data/operations.xlsx')
# print(profitable_categories_of_increased_cashback(data_file, 2021, 2))


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """
    Функция, возвращающая сумму, которую удалось бы отложить в «Инвесткопилку»
    :param month: месяц, для которого рассчитывается отложенная сумма в формате 'YYYY-MM'
    :type month: str
    :param transactions: список транзакций
    :type transactions: list[dict[str, Any]]
    :param limit: предел, до которого нужно округлять суммы операций
    :type limit: int
    :return: сумма, которую удалось бы отложить в «Инвесткопилку»
    :rtype: float
    """
    date = datetime.datetime.strptime(month + "-01", "%Y-%m-%d")
    start_date = datetime.datetime(date.year, date.month, 1, 0, 0, 0)
    if date.month == 12:
        end_date = datetime.datetime(date.year + 1, 1, 1, 23, 59, 59) - datetime.timedelta(days=1)
    else:
        end_date = datetime.datetime(date.year, date.month + 1, 1, 23, 59, 59) - datetime.timedelta(days=1)
    services_logger.debug(f"Вычисляем начальную ({start_date}) и конечную ({end_date}) даты")

    services_logger.debug("Сортируем операции по дате")
    data_filter_by_period = [
        dict_
        for dict_ in transactions
        if start_date <= datetime.datetime.strptime(dict_["Дата операции"], "%Y-%m-%d") <= end_date
    ]

    services_logger.debug("Вычисляем сумму округления")
    investment_sawmill = 0
    for transaction in data_filter_by_period:
        if transaction["Сумма операции"] < 0:
            summ_operation = abs(transaction["Сумма операции"])
            investment_sawmill += limit - summ_operation % limit

    services_logger.info("Возвращаем результат функции")
    return round(investment_sawmill, 2)

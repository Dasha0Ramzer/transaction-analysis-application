import datetime
import json
import logging
import os
from collections import Counter as cou
from typing import Any, Counter, Generator, Hashable

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(".env")

utils_logger = logging.getLogger("Вспомогательные функции")

logs_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
utils_handler = logging.FileHandler(os.path.join(logs_directory, 'utils.log'), mode="w", encoding="utf-8")

utils_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - Имя файла: %(filename)s - Имя функции: %(funcName)s \n%(levelname)s - %(message)s"
)
utils_handler.setFormatter(utils_formatter)
utils_logger.addHandler(utils_handler)
utils_logger.setLevel(logging.DEBUG)


def greeting(date_time_now: datetime.datetime) -> str:
    """
    Функция, возвращающая приветствие в соответствии с временем суток

    :param date_time_now: дата и время на данный момент
    :type date_time_now: 'datetime.datetime'
    :return: приветствие
    :rtype: str
    """
    hour = date_time_now.hour
    utils_logger.debug(f"Получаем часы суток ({hour})")
    utils_logger.info("Функция закончила работу")

    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


# print(greeting(datetime.datetime.now()))
# print(datetime.datetime.now())


def xlsx_file_reader(path_to_the_file: str) -> list[dict[Hashable, Any]]:
    """
    Функция, считывающая XLSX-файл и выводящая содержимое

    :param path_to_the_file: путь до XLSX-файла
    :type path_to_the_file: str
    :return: данные из файла
    :rtype: list[dict[Hashable, Any]]
    """
    utils_logger.debug("Считываем XLSX-файл с помощью pandas")
    transactions = pd.read_excel(path_to_the_file, engine='openpyxl')

    utils_logger.debug("Форматируем данные в словарь")
    data = transactions.to_dict(orient="records")

    utils_logger.info("Возвращаем содержимое файла operations.xlsx в виде списка словарей")
    return data


# print(xlsx_file_reader('../data/operations.xlsx'))


def filtering_by_date(data: list[dict[Hashable, Any]], date_time_now: datetime.datetime) -> list[dict[Hashable, Any]]:
    """
    Функция, фильтрующая транзакции в диапазоне с начала месяца по текущий день

    :param data: список транзакций
    :type data: list[dict[Hashable, Any]]
    :param date_time_now: дата и время на текущий момент
    :type date_time_now: 'datetime.datetime'
    :return: транзакции с начала месяца
    :rtype: list[dict[Hashable, Any]]
    """
    day_now = date_time_now.day
    month_now = date_time_now.month
    year_now = date_time_now.year
    utils_logger.debug(f"Получаем день ({day_now}) месяц ({month_now}) год ({year_now}) запроса к транзакциям")

    utils_logger.debug(
        "Формируем новый список словарей, в котором транзакции с первого числа месяца по запрашиваемую дату"
    )
    new_data = []
    for dict_ in data:
        date_of_operation = datetime.datetime.strptime(dict_["Дата операции"], "%d.%m.%Y %H:%M:%S")
        day_operation = date_of_operation.day
        month_operation = date_of_operation.month
        year_operation = date_of_operation.year
        if 1 <= day_operation <= day_now and month_operation == month_now and year_operation == year_now:
            new_data.append(dict_)

    utils_logger.debug("Сортируем новый список по дате по убыванию")
    result_data = sorted(new_data, key=lambda dictionary: dictionary["Дата операции"], reverse=True)

    utils_logger.info("Возвращаем отсортированные транзакции")
    return result_data


# date_obj = datetime.datetime(2021, 2, 12, 15, 45, 0)
# file_path = '../data/operations.xlsx'
# data_first = xlsx_file_reader(file_path)
# print(filtering_by_date(data_first, date_obj))


def cards(data: list[dict[Hashable, Any]]) -> Generator[str, None, None]:
    """
    Функция, выдающая номера всех карт

    :param data: список операций
    :type data: list[dict[Hashable, Any]]
    :return: генератор номер карты
    """
    utils_logger.info("Возвращаем номера карт")
    for dict_ in data:
        if isinstance(dict_["Номер карты"], str):
            yield dict_["Номер карты"]  # [1:]


# file_path = '../data/operations.xlsx'
# data_first = xlsx_file_reader(file_path)
# print(list(set(cards(data_first))))


def total_expenses(data: list[dict[Hashable, Any]], numbers_cards: list[str]) -> dict[str, float]:
    """
    Функция, суммирующая расходы за месяц

    :param data: список транзакций
    :type data: list[dict[Hashable, Any]]
    :param numbers_cards: номера всех карт
    :type numbers_cards: list[str]
    :return: словарь, где ключ - номер карты, значение - сумма расходов
    :rtype: dict[str, float]
    """
    category_counter: Counter[str] = cou()

    utils_logger.debug("Перебираем операции и суммируем расходы по каждой карте")
    for dict_ in data:
        card = dict_.get("Номер карты")
        if card in numbers_cards and dict_["Сумма платежа"] < 0:
            category_counter[card] += abs(dict_["Сумма платежа"])

    utils_logger.info("Возвращаем словарь с суммами расходов по каждой карте")
    return dict(category_counter)


# file_path = '../data/operations.xlsx'
# data_first = xlsx_file_reader(file_path)
# date_obj = datetime.datetime(2021, 2, 12, 15, 45, 0)
# print(total_expenses(filtering_by_date(data_first, date_obj), list(set(cards(data_first)))))


def cashback(expenditure: float) -> float:
    """
    Функция, рассчитывающая кэшбэк, исходя из суммы расходов

    :param expenditure:  расход
    :type expenditure: float
    :return: сумма кэшбэка, округленная до 2 знаков после запятой
    :rtype: float
    """
    utils_logger.info(f"Возвращаем кэшбэк: {expenditure} / 100 = {round(expenditure / 100, 2)}")
    return round(expenditure / 100, 2)


# file_path = '../data/operations.xlsx'
# data_first = xlsx_file_reader(file_path)
# date_obj = datetime.datetime(2021, 2, 12, 15, 45, 0)
# data_second = filtering_by_date(data_first, date_obj)
# total_expenses_ = total_expenses(data_second, list(set(cards(data_first))))
# print(total_expenses_['*7197'], cashback(total_expenses_['*7197']))
# print(total_expenses_['*4556'], cashback(total_expenses_['*4556']))


def top_transactions(data: list[dict[Hashable, Any]]) -> list[dict[str, Any]]:
    """
    Функция, возвращающая ТОП-5 транзакций по сумме операции

    :param data: список транзакций
    :type data: list[dict[Hashable, Any]]
    :return: ТОП-5 транзакций
    :rtype: list[dict[str, Any]]
    """
    utils_logger.debug("Сортируем транзакции по сумме платежа")
    sort_by_summ = sorted(data, key=lambda dictionary: abs(dictionary["Сумма платежа"]), reverse=True)

    utils_logger.debug("Отбираем 5 транзакций с самыми большими суммами платежа")
    top_5_transactions_ = sort_by_summ[:5]

    utils_logger.debug("Сортируем транзакции по дате по убыванию")
    top_transactions_ = sorted(top_5_transactions_, key=lambda dictionary: dictionary["Дата операции"], reverse=True)

    utils_logger.debug("Формируем список транзакций в соответствии с ТЗ")
    result = []
    for transaction in top_transactions_:
        result.append(
            {
                "date": transaction["Дата операции"][:10],
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )

    utils_logger.info("Возвращаем ТОП-5 транзакций по сумме платежа")
    return result


# file_path = '../data/operations.xlsx'
# data_first = xlsx_file_reader(file_path)
# date_obj = datetime.datetime(2021, 2, 12, 15, 45, 0)
# data_second = filtering_by_date(data_first, date_obj)
# print(top_transactions(data_second))


def exchange_rate() -> list[dict[str, Any]]:
    """
    Функция, возвращающая курс валют из файла user_settings.json

    :return: список словарей, где ключ - валюта пользователя, значение - курс этой валюты по отношению к рублю
    :rtype: list[dict[str, Any]]
    """
    utils_logger.debug("Получаем API-ключ из файла .env")
    api_key = os.getenv("API_KEY_1")
    headers = {"apikey": f"{api_key}"}
    url = "https://api.apilayer.com/exchangerates_data/latest"

    utils_logger.debug("Открываем файл с пользовательскими данными")
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_in_root = os.path.join(root_directory, 'user_settings.json')
    with open(file_in_root) as f:
        data = json.load(f)

    utils_logger.debug("Получаем из файла валюты пользователя")
    list_user_currencies = data["user_currencies"]

    utils_logger.debug("Получаем курс валют и формируем из этого список в соответствии с ТЗ")
    list_result = []
    for currency_ in list_user_currencies:
        payload = {"symbols": "RUB", "base": currency_}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            list_result.append({"currency": result["base"], "rate": round(result["rates"]["RUB"], 2)})
            utils_logger.debug(f'Валюта: {result["base"]}, стоимость: {round(result["rates"]["RUB"], 2)}')

    utils_logger.info("Возвращаем курс пользовательских валют")
    return list_result


# print(exchange_rate())


def stock_price() -> list[dict[str, Any]]:
    """
    Функция, возвращающая курс акций из файла user_settings.json

    :return: словарь, где ключ - акция пользователя, значение - курс этой акции
    :rtype: list[dict[str, Any]]
    """
    utils_logger.debug("Получаем API-ключ из файла .env")
    api_key = os.getenv("API_KEY_2")
    headers = {"X-Api-Key": f"{api_key}"}
    url = "https://api.api-ninjas.com/v1/stockprice"

    utils_logger.debug("Открываем файл с пользовательскими данными")
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_in_root = os.path.join(root_directory, 'user_settings.json')
    with open(file_in_root) as f:
        data = json.load(f)

    utils_logger.debug("Получаем из файла акции пользователя")
    list_user_stocks = data["user_stocks"]

    utils_logger.debug("Получаем курс акций и формируем из этого список в соответствии с ТЗ")
    list_result = []
    for stock_ in list_user_stocks:
        payload = {"ticker": stock_}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            list_result.append({"stock": result["ticker"], "price": round(result["price"], 2)})
            utils_logger.debug(f'Акция: {result["ticker"]}, стоимость: {round(result["price"], 2)}')

    utils_logger.info("Возвращаем курс пользовательских валют")
    return list_result


# print(stock_price())

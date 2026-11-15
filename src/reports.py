import datetime
import logging
import os
from functools import wraps
from typing import Any, Callable, Optional, Union

import pandas as pd

reports_logger = logging.getLogger("Основные функции для генерации JSON-ответов")

logs_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
reports_handler = logging.FileHandler(os.path.join(logs_directory, "reports.log"), mode="w", encoding="utf-8")

reports_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - Имя файла: %(filename)s - Имя функции: %(funcName)s \n%(levelname)s - %(message)s"
)
reports_handler.setFormatter(reports_formatter)
reports_logger.addHandler(reports_handler)
reports_logger.setLevel(logging.DEBUG)


def log() -> Callable[..., Any]:
    """Функция-декоратор, записывающая результат отчета в файл"""

    def decorator(func: Any) -> Any:
        """Декоратор для оборачивания функции функцией-оберткой"""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Функция-обертка"""
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = os.path.join(base_dir, "data", "decorator_result.json")
            # filename = '../data/decorator_result.json'
            try:
                message1 = f"Функция '{func.__name__}' начала работу с входными параметрами: {args}, {kwargs}"
                message2 = "Результат работы:"
                message3 = f"Функция '{func.__name__}' окончила работу успешно"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(message1 + "\n")
                result = func(*args, **kwargs)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(message2 + "\n" + str(result) + "\n")
                    f.write(message3 + "\n")
                return result

            except Exception as e:
                message4 = f"Произошла ошибка {e}"
                message5 = f"Функция '{func.__name__}' окончила работу"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(message4 + "\n")
                    f.write(message5 + "\n")
                raise

        return wrapper

    return decorator


@log()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[Union[str, datetime.datetime]] = None
) -> pd.DataFrame:
    """
    Функция, возвращающая траты по заданной категории за последние три месяца (от переданной даты)
    :param transactions: датафрейм с транзакциями
    :type transactions: pd.DataFrame
    :param category:название категории
    :type category: str
    :param date: опциональная дата
    :type date: Optional[Union[str, datetime.datetime]]
    :return: траты по заданной категории
    :rtype: pd.DataFrame
    """
    reports_logger.debug("Проверяем, вводилась ли дата и является ли она строкой")
    if date is None:
        date = datetime.datetime.now()
    elif isinstance(date, str):
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    reports_logger.debug("Отсчитываем 3 месяца назад")
    three_months_ago = date - datetime.timedelta(days=90)

    reports_logger.debug('Преобразовываем формат столбца "Дата операции" в формат datetime')
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    reports_logger.debug("Фильтруем транзакции по дате и по категории")
    filtering_transactions = transactions[
        (transactions["Категория"] == category)
        & (three_months_ago <= transactions["Дата операции"])
        & (transactions["Дата операции"] <= date)
        & (transactions["Сумма операции"] < 0)
    ]

    reports_logger.info("Возвращаем результат функции")
    return filtering_transactions


@log()
def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[Union[str, datetime.datetime]] = None
) -> pd.DataFrame:
    """
    Функция, возвращающая средние траты в каждый из дней недели за последние три месяца (от переданной даты)
    :param transactions: датафрейм с транзакциями
    :type transactions: pd.DataFrame
    :param date: опциональная дата
    :type date: Optional[Union[str, datetime.datetime]]
    :return: средние траты на каждый день недели
    :rtype: pd.DataFrame
    """
    reports_logger.debug("Проверяем, вводилась ли дата и является ли она строкой")
    if date is None:
        date = datetime.datetime.now()
    elif isinstance(date, str):
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    reports_logger.debug("Отсчитываем 3 месяца назад")
    three_months_ago = date - datetime.timedelta(days=90)

    reports_logger.debug('Преобразовываем формат столбца "Дата операции" в формат datetime')
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    reports_logger.debug("Фильтруем транзакции по дате")
    filtering_transactions = transactions[
        (three_months_ago <= transactions["Дата операции"])
        & (transactions["Дата операции"] <= date)
        & (transactions["Сумма операции"] < 0)
    ]

    reports_logger.debug('Добавляем столбец "День недели"')
    filtering_transactions["День недели"] = filtering_transactions["Дата операции"].dt.day_name()

    filtering_transactions["Сумма операции"] = filtering_transactions["Сумма операции"].abs()

    reports_logger.debug("Вычисляем среднее значение по дню недели")
    result = filtering_transactions.groupby("День недели")["Сумма операции"].mean().reset_index()

    reports_logger.info("Возвращаем результат функции")
    return result


@log()
def spending_by_workday(
    transactions: pd.DataFrame, date: Optional[Union[str, datetime.datetime]] = None
) -> pd.DataFrame:
    """
    Функция, возвращающая средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)
    :param transactions: датафрейм с транзакциями
    :type transactions: pd.DataFrame
    :param date: опциональная дата
    :type date: Optional[Union[str, datetime.datetime]]
    :return: средние траты на рабочий и выходной дни
    :rtype: pd.DataFrame
    """
    reports_logger.debug("Проверяем, вводилась ли дата и является ли она строкой")
    if date is None:
        date = datetime.datetime.now()
    elif isinstance(date, str):
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    reports_logger.debug("Отсчитываем 3 месяца назад")
    three_months_ago = date - datetime.timedelta(days=90)

    reports_logger.debug('Преобразовываем формат столбца "Дата операции" в формат datetime')
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    reports_logger.debug("Фильтруем транзакции по дате")
    filtering_transactions = transactions[
        (three_months_ago <= transactions["Дата операции"])
        & (transactions["Дата операции"] <= date)
        & (transactions["Сумма операции"] < 0)
    ]

    reports_logger.debug('Добавляем столбец "Тип дня"')
    filtering_transactions["Тип дня"] = filtering_transactions["Дата операции"].dt.weekday.apply(
        lambda x: "Рабочий" if x < 5 else "Выходной"
    )

    filtering_transactions["Сумма операции"] = filtering_transactions["Сумма операции"].abs()

    reports_logger.debug("Вычисляем среднее значение по типу дня")
    result = filtering_transactions.groupby("Тип дня")["Сумма операции"].mean().reset_index()

    reports_logger.info("Возвращаем результат функции")
    return result

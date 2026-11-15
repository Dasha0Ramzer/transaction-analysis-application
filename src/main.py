from datetime import datetime
from typing import Any

import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import (
    investment_bank,
    profitable_categories_of_increased_cashback,
    search_by_phone_numbers,
    search_for_transfers_to_individuals,
    simple_search,
)
from src.utils import xlsx_file_reader
from src.views import create_json_data_events_page, create_json_data_home_page


def main() -> Any:
    print("Добро пожаловать!")
    while True:
        print()
        web_home_page = input(
            'Введите дату и время для отображения на странице "Главная" в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС : '
        )
        try:
            datetime.strptime(web_home_page, "%Y-%m-%d %H:%M:%S")
            print(create_json_data_home_page(web_home_page))
            break
        except ValueError:
            print("Формат даты и времени неверный. Пожалуйста, используйте формат ГГГГ-ММ-ДД ЧЧ:ММ:СС.")

    while True:
        print()
        web_events_page = input(
            'Введите дату и время для отображения на странице "События" в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС : '
        )
        try:
            datetime.strptime(web_events_page, "%Y-%m-%d %H:%M:%S")
            break
        except ValueError:
            print("Формат даты и времени неверный. Пожалуйста, используйте формат ГГГГ-ММ-ДД ЧЧ:ММ:СС.")
    while True:
        print()
        web_events_page_period = input(
            "Диапазон данных по умолчанию - 1 месяц. Хотите изменить диапазон данных? Введите да/нет: "
        )
        if web_events_page_period.lower() == "да":
            print("""
            Возможные значения диапазона:
            W — неделя, на которую приходится дата;
            M — месяц, на который приходится дата;
            Y — год, на который приходится дата;
            ALL — все данные до указанной даты.
            """)
            web_events_page_period = input("Введите диапазон: ")
            print(create_json_data_events_page(web_events_page, web_events_page_period))
            break
        elif web_events_page_period.lower() == "нет":
            print(create_json_data_events_page(web_events_page))
            break
        else:
            print("Пожалуйста, повторите ввод.")

    while True:
        print("""
        На выбор предоставляется несколько сервисов:
        1. Выгодные категории повышенного кешбэка
        2. Инвесткопилка
        3. Простой поиск
        4. Поиск по телефонным номерам
        5. Поиск переводов физическим лицам""")
        services_ansver = input("Хотите воспользоваться одним из сервисов? Введите да/нет: ")
        if services_ansver.lower() == "да":
            while True:
                services_ansver = input("Введите порядковый номер сервиса: ")
                if services_ansver in "12345":
                    break
                else:
                    print("Пожалуйста, повторите ввод.")
            break
        elif services_ansver.lower() == "нет":
            break
        else:
            print("Пожалуйста, повторите ввод.")

    print()
    if services_ansver == "1":
        print('Вы выбрали сервис "Выгодные категории повышенного кешбэка".')
        while True:
            services_ansver_year = input("Введите год для анализа: ")
            if services_ansver_year.isdigit() and len(services_ansver_year) == 4:
                break
            else:
                print("Пожалуйста, повторите ввод.")
        while True:
            services_ansver_month = input("Введите порядковый номер месяца для анализа: ")
            if services_ansver_month.isdigit() and len(services_ansver_month) == 2:
                break
            else:
                print("Пожалуйста, повторите ввод.")
        print(f"Выгодные категории повышенного кешбэка в {services_ansver_month}.{services_ansver_year}:")
        print(
            profitable_categories_of_increased_cashback(
                xlsx_file_reader("../data/operations.xlsx"), int(services_ansver_year), int(services_ansver_month)
            )
        )

    elif services_ansver == "2":
        print('Вы выбрали сервис "Инвесткопилка".')
        while True:
            services_ansver_date = input(
                'Введите месяц, для которого рассчитывается отложенная сумма в формате "ГГГГ-MM"'
            )
            try:
                datetime.strptime(services_ansver_date, "%Y-%m")
                break
            except ValueError:
                print("Формат даты неверный. Пожалуйста, используйте формат ГГГГ-ММ.")
        while True:
            services_ansver_limit = input("Введите предел, до которого нужно округлять суммы операций: ")
            if services_ansver_limit.isdigit():
                break
            else:
                print("Пожалуйста, повторите ввод.")
        print("Сумма, которую удалось бы отложить в «Инвесткопилку»: ", end="")
        print(
            investment_bank(
                services_ansver_date, xlsx_file_reader("../data/operations.xlsx"), int(services_ansver_limit)
            )
        )

    elif services_ansver == "3":
        print('Вы выбрали сервис "Простой поиск".')
        services_ansver_request = input("Ведите запрос для поиска: ")
        if simple_search(services_ansver_request, xlsx_file_reader("../data/operations.xlsx")) == "[]":
            print("Нет транзакций, подходящих под запрос.")
        else:
            print(simple_search(services_ansver_request, xlsx_file_reader("../data/operations.xlsx")))

    elif services_ansver == "4":
        print('Вы выбрали сервис "Поиск по телефонным номерам".')
        print(search_by_phone_numbers(xlsx_file_reader("../data/operations.xlsx")))

    elif services_ansver == "5":
        print('Вы выбрали сервис "Поиск переводов физическим лицам".')
        print(search_for_transfers_to_individuals(xlsx_file_reader("../data/operations.xlsx")))

    print()
    while True:
        print("""
        На выбор предоставляется несколько отчетов:
        1. Траты по категории
        2. Траты по дням недели
        3. Траты в рабочий/выходной день""")
        reports_ansver = input("Хотите получить один из отчетов? Введите да/нет: ")
        if reports_ansver.lower() == "да":
            while True:
                reports_ansver = input("Введите порядковый номер отчета: ")
                if reports_ansver in "123":
                    break
                else:
                    print("Пожалуйста, повторите ввод.")
            break
        elif reports_ansver.lower() == "нет":
            break
        else:
            print("Пожалуйста, повторите ввод.")

    print()
    if reports_ansver == "1":
        print('Вы выбрали отчет "Траты по категории".')
        reports_ansver_category = input("Введите категорию для отчета: ")
        while True:
            reports_ansver_date = input("""
            Опциональная дата по умолчанию - сегодня.
            Если хотите ее изменить, то введите новую дату в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС, иначе нажмите "Enter" : """)
            if reports_ansver_date == "":
                reports_ansver_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                break
            else:
                try:
                    datetime.strptime(reports_ansver_date, "%d.%m.%Y %H:%M:%S")
                    break
                except ValueError:
                    print("Формат даты неверный. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ:СС.")
        data_list = xlsx_file_reader("../data/operations.xlsx")
        transactions_df = pd.DataFrame(data_list)
        print(f"""Траты по категории {reports_ansver_category} за последние 3 месяца
            находятся в папке "data" под названием "decorator_result.json".""")
        spending_by_category(transactions_df, reports_ansver_date)

    print()
    if reports_ansver == "2":
        print('Вы выбрали отчет "Траты по дням недели".')
        while True:
            reports_ansver_date = input("""Опциональная дата по умолчанию - сегодня.
                Если хотите ее изменить, введите новую дату в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС, иначе нажмите "Enter" : """)
            if reports_ansver_date == "":
                reports_ansver_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                break
            else:
                try:
                    datetime.strptime(reports_ansver_date, "%d.%m.%Y %H:%M:%S")
                    break
                except ValueError:
                    print("Формат даты неверный. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ:СС.")
        data_list = xlsx_file_reader("../data/operations.xlsx")
        transactions_df = pd.DataFrame(data_list)
        print("""Средние траты по дням недели за последние 3 месяца
            находятся в папке "data" под названием "decorator_result.json".""")
        spending_by_weekday(transactions_df, reports_ansver_date)

    print()
    if reports_ansver == "3":
        print('Вы выбрали отчет "Траты в рабочий/выходной день".')
        while True:
            reports_ansver_date = input("""Опциональная дата по умолчанию - сегодня.
                Если хотите ее изменить, введите новую дату в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС, иначе нажмите "Enter" : """)
            if reports_ansver_date == "":
                reports_ansver_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                break
            else:
                try:
                    datetime.strptime(reports_ansver_date, "%d.%m.%Y %H:%M:%S")
                    break
                except ValueError:
                    print("Формат даты неверный. Пожалуйста, используйте формат ДД.ММ.ГГГГ ЧЧ:ММ:СС.")
        data_list = xlsx_file_reader("../data/operations.xlsx")
        transactions_df = pd.DataFrame(data_list)
        print("""Средние траты в рабочий и выходной дни за последние 3 месяца
            находятся в папке "data" под названием "decorator_result.json".""")
        spending_by_workday(transactions_df, reports_ansver_date)

    print("Благодарим Вас за пользование нашим сервисом.")


main()

from pathlib import Path

from prettytable import PrettyTable

from src.api_clients import HeadHunterAPI
from src.api_clients.base import VacancyApiClient
from src.file_connector import JSONConnector
from src.file_connector.base import FileConnector

BASE_PATH = Path(__file__).parent
VACANCIES_PATH_FILE = BASE_PATH.joinpath('vacancies.json')

api_client: VacancyApiClient = HeadHunterAPI()
json_connector: FileConnector = JSONConnector(VACANCIES_PATH_FILE)

WELCOME_MESSAGE = """
Добро пожаловать в программу!
Выберите действия:
    1.Ввести поисковый запрос для запроса вакансий из hh.ru;
    2.Получить топ вакансий по зарплате;
    3.Получить вакансии с ключевым словом в описании;
    4.Выйти из программы.
    """


def for_1():
    vacancies = json_connector.get_vacancies()
    for vac in vacancies:
        json_connector.delete_vacancy(vac)

    search_word = input('Введите слово для поиска:')
    vacancies = api_client.get_vacancies(search_word.lower())
    for vac in vacancies:
        if search_word.lower() in vac.name:
            json_connector.add_vacancy(vac)
            print(vac)


def for_2():
    users_top = int(input('Введите количество вакансий:'))
    vacancies = json_connector.get_vacancies()
    t = PrettyTable(['name', 'url', 'emloyer', 'salary'])
    for vac in sorted(vacancies, key=lambda x: x.salary, reverse=True)[:users_top]:
        salary = '{_from} -> {_to}, {currency}'.format(
            _from=vac.salary.salary_from or 0,
            _to=vac.salary.salary_to or 0,
            currency=vac.salary.currency
        )
        t.add_row([vac.name, vac.url, vac.employer_name, salary])
    print(t)


def for_3():
    search_word = input('Введите слово для поиска в описании вакансии:')
    vacancies = json_connector.get_vacancies()
    t = PrettyTable(['name', 'url', 'emloyer', 'salary', 'snippet'])
    for vac in vacancies:
        salary = '{_from} -> {_to}, {currency}'.format(
            _from=vac.salary.salary_from or 0,
            _to=vac.salary.salary_to or 0,
            currency=vac.salary.currency
        )

        if search_word in vac.snippet:
            t.add_row([vac.name, vac.url, vac.employer_name, salary, vac.snippet])
    print(t)


MAPPING = {'1': for_1, '2': for_2, '3': for_3}


def main():
    while True:
        print(WELCOME_MESSAGE)
        user_input = input()
        if not user_input.isdigit():
            continue
        if user_input in MAPPING:
            callback = MAPPING[user_input]
            callback()
        elif user_input == '4':
            break


if __name__ == '__main__':
    main()

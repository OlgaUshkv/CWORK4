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


def get_request_vacancies():
    """
    Получаем список вакансий по запросу из HH.ru
    """
    vacancies = json_connector.get_vacancies()
    for vac in vacancies:
        json_connector.delete_vacancy(vac)

    search_word = input('Введите слово для поиска:')
    vacancies = api_client.get_vacancies(search_word.lower())
    for vac in vacancies:
        if search_word.lower() in vac.name:
            json_connector.add_vacancy(vac)
            #print(vac)


def get_count_vacancies():
    """
    Получаем ТОП вакансий по зарплате
    """
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


def get_actual_vacancy():
    """
    Получаем список вакансий по ключевому слову в описании
    """
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

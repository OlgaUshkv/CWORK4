import requests
from .base import VacancyApiClient
from ..dto import Vacancy, Salary


class HeadHunterAPI(VacancyApiClient):

    def get_vacancies(self, search_text: str) -> list[Vacancy]:
        url = 'https://api.hh.ru/vacancies/'
        params = {
            'only_with_salary': True,
            'per_page': 100,
            'text': search_text
        }

        response = requests.get(url, params=params, timeout=10)
        if not response.ok:
            print(f'Ошибка получения данных с HH.ru, {response.content}')
            return []

        return [
            self._parse_vacancy_data(item) for item in response.json()['items']
        ]

    def _parse_vacancy_data(self, data: dict) -> Vacancy:
        return Vacancy(
            name=data['name'],
            url=data['alternate_url'],
            employer_name=data['employer']['name'],
            snippet=data['snippet']['requirement'],
            salary=Salary(
                salary_from=data['salary']['from'],
                salary_to=data['salary']['to'],
                currency=data['salary']['currency']
            )
        )

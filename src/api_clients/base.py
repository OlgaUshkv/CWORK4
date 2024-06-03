from abc import ABC, abstractmethod

from src.dto import Vacancy


class VacancyApiClient(ABC):

    @abstractmethod
    def get_vacancies(self, search_text: str) -> list[Vacancy]:
        pass

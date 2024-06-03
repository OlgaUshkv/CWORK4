from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Salary:
    currency: str
    salary_from: int | None = None
    salary_to: int | None = None

    def __lt__(self, other):
        self_salary_from = self.salary_from or 0
        self_salary_to = self.salary_to or 0
        other_salary_from = other.salary_from or 0
        other_salary_to = other.salary_to or 0

        if 0 not in (self_salary_from, other_salary_from):
            if self_salary_from == other_salary_from:
                return self_salary_to < other_salary_to
            return self_salary_from < other_salary_from

        if self_salary_from == 0 and other_salary_from == 0:
            return True

        if None in (self.salary_from, other.salary_from):
            return True

        return False


@dataclass(unsafe_hash=True)
class Vacancy:
    name: str
    url: str
    employer_name: str
    snippet: str
    salary: Salary

    def __lt__(self, other):
        return self.salary < other.salary


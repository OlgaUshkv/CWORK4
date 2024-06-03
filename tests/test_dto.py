from src.dto import Salary


class TestSalaryCompare:

    def test_salary_are_equals_none_with_same_currency(self):
        salary_1 = Salary(salary_from=None, salary_to=None, currency='RUR')
        salary_2 = Salary(salary_from=None, salary_to=None, currency='RUR')

        assert salary_1 == salary_2

    def test_salary_are_equals_not_none_with_same_currency(self):
        salary_1 = Salary(salary_from=200, salary_to=2_000, currency='RUR')
        salary_2 = Salary(salary_from=200, salary_to=2_000, currency='RUR')

        assert salary_1 == salary_2

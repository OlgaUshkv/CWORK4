from src.utils import get_request_vacancies, get_count_vacancies, get_actual_vacancy

WELCOME_MESSAGE = """
Добро пожаловать в программу!
Выберите действия:
    1.Ввести поисковый запрос для запроса вакансий из hh.ru;
    2.Получить топ вакансий по зарплате;
    3.Получить вакансии с ключевым словом в описании;
    4.Выйти из программы.
    """

MAPPING = {'1': get_request_vacancies, '2': get_count_vacancies, '3': get_actual_vacancy}


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

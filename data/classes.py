import random
import requests
import json
from data import errors as Error, utils as script


class HeadHunter:
    """
    Класс получения и кэширования информации с сайта hh.ru
    """
    counter = 0  # Для перебора по страницам, перебор начинается с 0 страницы
    def __init__(self, vacancy_name, v_count=100):
        """
        :param v_count: Количество вакансий, не более 20 на 1 странице!.
        :param vacancy_name: Название искомой вакансии
        """
        while self.counter != 10:
            parametres = {'per_page': v_count, 'page': self.counter}
            self.vacancy_list = requests.get(f'https://api.hh.ru/vacancies?text={vacancy_name}'
                                   f'&area=1'
                                   f'&search_field=name',
                                   parametres)

            if self.vacancy_list.status_code == 200:
                vacancy_list = self.vacancy_list.json()
                script.package(vacancy_list, Vacancy)
            self.counter += 1


class SuperJob:
    """
    Класс обработки получаемой информации с сайта superjob.ru
    """
    counter = 0  # Для перебора по страницам, перебор начинается с 0 страницы
    def __init__(self, vacancy_name, v_count=100):
        """
        :param vacancy_name: Название вакансии
        """
        api_key = script.api_loader()
        headers = {"X-Api-App-Id": api_key}  # Можно ввести свой ключ сюда
        while self.counter != 10:  # Цикл для выдачи вакансий больше чем позволяет API
            params = {"keyword": f"{vacancy_name}",
                  "count": v_count,
                  "page":self.counter}  # Счетчик вставляем в страницу, чтобы вакансии обновлялись при запросе
            self.vacancy_list = requests.get(f'https://api.superjob.ru/2.0/vacancies/',
                                             headers=headers,
                                             params=params)

            if self.vacancy_list.status_code == 200:
                vacancy_list = self.vacancy_list.json()
                script.package(vacancy_list, Vacancy)
            self.counter += 1


class Vacancy:
    """
    Класс работы с вакансиями
    """

    vacancy_dict = {}
    vacancy_list = []
    num_id = 0
    like_id = []

    def __init__(self, name):
        """
        :param name: Название профессии
        """
        self.name = name

    def start(self):
        """
        Инициализирует классы HeadHunter и SuperJob
        """
        HeadHunter(self.name), SuperJob(self.name)

    def __str__(self):
        """
        :return: Вывод информации
        """
        with open('../last_search.json', 'w', encoding='UTF-8') as last_vac:
            try:
                    random_vacancy = self.vacancy_dict['items'][random.randint(0, len(self.vacancy_dict['items']))]
                    x = json.dumps(random_vacancy, indent=2, ensure_ascii=False)
                    last_vac.write(x)
            except IndexError:
                raise Error.UnknowVacancie()
            try:
                return f'Вакансия: {random_vacancy["vacancy_name"]}\n' \
                   f'Описание: {random_vacancy["vacancy_description"]}\n' \
                   f'Зарплата: от {random_vacancy["vacancy_salary"]["from"]} ' \
                   f'до {random_vacancy["vacancy_salary"]["to"]} {random_vacancy["vacancy_salary"]["cur"]}\n' \
                   f'Ссылка: {random_vacancy["vacancy_url"]}\n' \
                   f'Работодатель: {random_vacancy["vacancy_emp"]}'
            except Exception:
                raise Error.UnknowVacancie()

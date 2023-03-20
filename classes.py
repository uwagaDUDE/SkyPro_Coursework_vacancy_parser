import os
import random

import requests
import json
import utils as script

class SearchedVacancy:
    def __init__(self, vacancy_name):
        """
        :param vacancy_name: Название искомой вакансии
        """
        self.vacancy_name = vacancy_name


class Vacancy:
    """
    Класс работы с вакансиями, содержит в себе классы HeadHunter и SuperJob
    """

    vacancy_dict = {}
    vacancy_list = []
    num_id = 0
    class HeadHunter(SearchedVacancy):
        """
        Класс получения и кэширования информации с сайта hh.ru
        """
        counter = 0 # Для перебора по страницам, перебор начинается с 0 страницы
        def __init__(self, vacancy_name, v_count=100):
            """
            :param v_count: Количество вакансий, не более 20 на 1 странице!.
            :param v_page: Количество страниц, на 1 странице не более 20 вакансий.
            :param vacancy_name: Название искомой вакансии
            """
            super().__init__(vacancy_name)
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

    class SuperJob(SearchedVacancy):
        """
        Класс обработки получаемой информации с сайта superjob.ru
        """
        counter = 0  # Для перебора по страницам, перебор начинается с 0 страницы
        def __init__(self, vacancy_name, v_count=100):
            """
            :param vacancy_name: Название вакансии
            """
            super().__init__(vacancy_name)

            api_key = script.api_loader()
            headers = {"X-Api-App-Id": api_key}
            while self.counter != 10:
                params = {"keyword": f"{vacancy_name}",
                      "count": v_count,
                      "page":self.counter}
                self.vacancy_list = requests.get(f'https://api.superjob.ru/2.0/vacancies/',
                                                 headers=headers,
                                                 params=params)

                if self.vacancy_list.status_code == 200:
                    vacancy_list = self.vacancy_list.json()
                    script.package(vacancy_list, Vacancy)
                self.counter += 1

    def __init__(self, name):
        """
        :param name: Название профессии
        """
        self.name = name

    def start(self):
        """
        Инициализирует классы HeadHunter и SuperJob
        """
        self.HeadHunter(self.name), self.SuperJob(self.name)

    def __str__(self):
        """
        :return: Вывод информации
        """
        with open('last_search.json', 'w', encoding='UTF-8') as last_vac:
            try:
                    random_vacancy = self.vacancy_dict['items'][random.randint(0, len(self.vacancy_dict['items']))]
                    x = json.dumps(random_vacancy, indent=2, ensure_ascii=False)
                    last_vac.write(x)
            except IndexError:
                raise AllErrors.UnknowVacancie()
            try:
                return f'Вакансия: {random_vacancy["vacancy_name"]}\n' \
                   f'Описание: {random_vacancy["vacancy_description"]}\n' \
                   f'Зарплата: от {random_vacancy["vacancy_salary"]["from"]} ' \
                   f'до {random_vacancy["vacancy_salary"]["to"]} {random_vacancy["vacancy_salary"]["cur"]}\n' \
                   f'Ссылка: {random_vacancy["vacancy_url"]}'
            except Exception:
                raise AllErrors.UnknowVacancie()


class AllErrors(Exception):
    """
    Класс включающий в себя классы ошибок
    """
    class ApiKeyError(Exception):
        """
        Ошибка ввода ключа
        """
        def __init__(self, api_key):
            """
            :param api_key: API ключ
            """
            if api_key == None:
                raise Exception(f'Ошибка ввода ключа, попробуйте ввести его вручную.')

    class CacheError(Exception):
        def __init__(self):
            raise Exception(f'Файла с кэшом не найдено.')

    class WrongInput(Exception):
        def __init__(self):
            raise Exception(f'Ошибка ввода! Вводите только цифры!')

    class WrongMaxValue(Exception):
        def __init__(self):
            raise Exception(f'Вакансий должно быть не больше 20 на 1 странице!')

    class WrongMaxVacancies(Exception):
        def __init__(self):
            raise Exception(f'Всего количество вакансий не должно превышать 2000!')

    class UnknowVacancie(Exception):
        def __init__(self):
            raise Exception(f'Такой вакансии не найдено.')
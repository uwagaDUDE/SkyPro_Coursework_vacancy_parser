import os
import requests
import json
import utils as script


class VacancyCache:
    """
    Работа с файлами связанными с вакансиями
    """
    def __init__(self):
        """
        Проверяем наличие папки для хранения вакансий
        """
        if os.path.exists('./.cache'):
            #Проверяем наличие папки хранящей вакансии с hh.ru
            if os.path.exists('./.cache/HHru'):
                pass
            else:
                os.mkdir('./.cache/HHru')
            #Проверяем наличие папки хранящей вакансии с Superjob
            if os.path.exists('./.cache/Superjob'):
                pass
            else:
                os.mkdir('./.cache/Superjob')
        else:
            os.mkdir('./.cache')
            os.mkdir('./.cache/Superjob')
            os.mkdir('./.cache/HHru')


class SearchedVacancy:
    def __init__(self, vacancy_name):
        """
        :param vacancy_name: Название искомой вакансии
        """
        self.vacancy_name = vacancy_name


class HeadHunterParse(SearchedVacancy):
    """
    Класс получения и кэширования информации с сайта hh.ru
    """
    def __init__(self, vacancy_name, v_count=10, v_page=1):
        """
        :param v_count: Количество вакансий, не более 20 на 1 странице!.
        :param v_page: Количество страниц, на 1 странице не более 20 вакансий.
        :param vacancy_name: Название искомой вакансии
        """
        super().__init__(vacancy_name)
        parametres = {'per_page':v_count,'page':v_page}
        request = requests.get(f'https://api.hh.ru/vacancies?text={vacancy_name}'
                                         f'&area=1'
                                         f'&search_field=name',
                                         parametres)

        if request.status_code == 200:
            script.open_file('HHru', request)
        else:
            print('Ошибка подключения.')


class SuperJob(SearchedVacancy):
    """
    Класс обработки получаемой информации с сайта superjob.ru
    """
    def __init__(self, vacancy_name):
        """
        :param vacancy_name: Название вакансии
        """
        super().__init__(vacancy_name)
        api_key = script.api_loader()
        headers = {"X-Api-App-Id": api_key}
        params = {"keyword": f"{vacancy_name}"}
        self.vacancy_list = requests.get(f'https://api.superjob.ru/2.0/vacancies/',
                                         headers=headers,
                                         params=params)

        if self.vacancy_list.status_code == 200:
            script.open_file('Superjob', self.vacancy_list)
        else:
            print('Ошибка подключения')


class GetVacancy(HeadHunterParse, SuperJob, VacancyCache):
    """
    Вывод вакансий с HH.ru и SuperJob.ru
    """
    vacancy_names = []
    vacancy_desc = []
    vacancy_urls = []
    vacancy_salary_from = []
    vacancy_salary_to = []
    salary_curr = []
    vacancy_dict = {}
    tick = -1

    def __init__(self, vacancy_name, v_count, v_page):
        """
        :param v_count: Количество вакансий (не более 20 на 1 страницу)
        :param v_page: Количество страниц
        """
        super().__init__(vacancy_name, v_count=v_count, v_page=v_page)
        super(HeadHunterParse, self).__init__(vacancy_name)
        super(SuperJob, self).__init__(vacancy_name)

    def vacancy_package(self):
        """
        Упаковываем данные в удобный для работы словарь
        :return:
        """
        for package in range(0, len(self.vacancy_names)):
            self.vacancy_dict[package] = {
                'vacancy_name':self.vacancy_names[package],
                'vacancy_description':self.vacancy_desc[package],
                'vacancy_salary':{'from':self.vacancy_salary_from[package],
                                  'to':self.vacancy_salary_to[package],
                                  'cur':self.salary_curr[package]},
                'vacancy_url':self.vacancy_urls[package]
            }
        with open('last_search.json', 'w', encoding='UTF-8') as package:
            package.write(json.dumps(self.vacancy_dict, indent=2, ensure_ascii=False))

    def get_hh(self):
        """
        Заполняем атрибуты vacancy_names, vacancy_desc, vacancy_urls, vacancy_salary содержимым c hh.ru
        :return:
        """
        with open('./.cache/HHru/vacancy_list.json', 'r', encoding='UTF-8') as hh_file:
            hh_json = json.load(hh_file)
            script.get_vacancy_information(hh_json, self.vacancy_names, self.vacancy_urls, self.vacancy_desc,
                                           self.vacancy_salary_from, self.vacancy_salary_to, self.salary_curr)

    def get_sj(self):
        """
        Заполняем атрибуты vacancy_names, vacancy_desc, vacancy_urls, vacancy_salary содержимым c superjob.ru
        :return:
        """
        with open('./.cache/Superjob/vacancy_list.json', 'r', encoding='UTF-8') as sj:
            sj_json = json.load(sj)
            script.get_vacancy_information(sj_json, self.vacancy_names, self.vacancy_desc, self.vacancy_urls,
                                           self.vacancy_salary_from, self.vacancy_salary_to, self.salary_curr)

    def parse(self):
        """
        Объединение двух методов
        :return:
        """
        self.get_hh()
        self.get_sj()

    def __str__(self):
        """
        Вывод информации
        :return:
        """
        with open('last_search.json', 'r', encoding='UTF-8') as loader:
            search = json.load(loader)
            try:
                self.tick = self.tick+1
                tick = self.tick
                return f'\n' \
                     f'Вакансия: {search[str(tick)]["vacancy_name"]}\n' \
                       f'Описание: {search[str(tick)]["vacancy_description"]}\n' \
                       f'Заработная плата: от {search[str(tick)]["vacancy_salary"]["from"]} ' \
                       f'до {search[str(tick)]["vacancy_salary"]["to"]} {search[str(tick)]["vacancy_salary"]["cur"]}\n' \
                       f'Ссылка на вакансию: {search[str(tick)]["vacancy_url"]}'
            except Exception:
                return f'Ошибка вывода информации'


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
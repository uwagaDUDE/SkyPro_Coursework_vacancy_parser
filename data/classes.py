import random
import requests
import json
from data import errors as Error, utils as script
import psycopg2

class DataBase:

    """
    Класс работы с базами данных
    """

    def __init__(self, admin_password,
                 admin_name='postgres',
                 database='Vacancy',
                 host='localhost',
                 port='5432'):

        """
        :param admin_password: Пароль от супер-пользователя
        :param admin_name: Логин супер-пользователя (default = postgres)
        :param database: База данных (default = Vacancy)
        :param host: IP (default = localhost)
        :param port: PORT (default = 5432)
        """

        self.connection = psycopg2.connect(database=database,
                                           user=admin_name,
                                           password=admin_password,
                                           host=host, port=port)

        self.connection.autocommit = True
        self.cur = self.connection.cursor()
        #  Проверяем наличие БД
        self.cur.execute("SELECT datname FROM pg_database WHERE datname='vacancy'")
        exists = self.cur.fetchone()
        if exists:
            pass
        else:
            try:
                self.cur.execute('CREATE DATABASE Vacancy')  # создаем базу данных для хранения вакансий
                self.cur.execute('CREATE TABLE founded_vacancy'  # создаем таблицу SQL для хранения найденных выкансий
                            '('
                            'ID SERIAL PRIMARY KEY,'
                            'Vacancy_name varchar(255),'
                            'Vacancy_description varchar(255),'
                            'Vacancy_Salary_max int,'
                            'Vacancy_Salary_min int,'
                            'Vacancy_Salary_cur varchar(25),'
                            'Vacancy_Salary_url varchar(255)'
                            ')')
                self.cur.execute('')
            except Exception:
                print('Sho')
                pass

    def cursor(self):
        return self.cur
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
                script.package(vacancy_list, Vacancy, DataBase('5772').cursor())
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
                script.package(vacancy_list, Vacancy, DataBase('5772').cursor())
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

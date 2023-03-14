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
        self.vacancy_list = requests.get(f'https://api.hh.ru/vacancies?text={vacancy_name}'
                                         f'&area=1'
                                         f'&search_field=name',
                                         parametres)
        if self.vacancy_list.status_code == 200:

            try:
                with open('./.cache/HHru/vacancy_list.json', 'w', encoding='UTF-8') as hh:
                    vacancy_json = self.vacancy_list.json()
                    hh.write(json.dumps(vacancy_json, indent=2, ensure_ascii=False))

            except Exception as Error:
                print(f'Произошла ошибка:'
                      f'{Error}')
        else:
            print('Ошибка подключения.')


class SuperJob(SearchedVacancy):
    """
    Класс обработки получаемой информации с сайта superjob.ru
    """
    def __init__(self, vacancy_name):
        super().__init__(vacancy_name)
        api_key = script.api_loader()
        headers = {"X-Api-App-Id": api_key}
        params = {"keyword": f"{vacancy_name}"}
        self.vacancy_list = requests.get(f'https://api.superjob.ru/2.0/vacancies/',
                                         headers=headers,
                                         params=params)

        if self.vacancy_list.status_code == 200:
            with open('./.cache/Superjob/vacancy_list.json', 'w', encoding='UTF-8') as sj:
                vacancy_json = self.vacancy_list.json()
                sj.write(json.dumps(vacancy_json, indent=2, ensure_ascii=False))
        else:
            print('Ошибка подключения')


class GetVacancy(HeadHunterParse, SuperJob, VacancyCache):
    """
    Вывод вакансий с HH.ru и SuperJob.ru
    """
    vacancy_names = []
    vacancy_desc = []
    vacancy_urls = []
    vacancy_salary = []
    def __init__(self, vacancy_name, v_count, v_page):
        """
        :param v_count: Количество вакансий (не более 20 на 1 страницу)
        :param v_page: Количество страниц
        """
        super().__init__(vacancy_name, v_count=v_count, v_page=v_page)
        super(HeadHunterParse, self).__init__(vacancy_name)
        super(SuperJob, self).__init__(vacancy_name)
        self.vacancy_name = ''
        self.vacancy_description = ''
        self.vacancy_url = ''
        self.vacancy_money = ''

    def get_hh(self):
        with open('./.cache/HHru/vacancy_list.json', 'r', encoding='UTF-8') as hh:
            hh_json = json.load(hh)

            for vacs in hh_json['items']:

                self.vacancy_names.append(vacs['name'])
                try:
                    self.vacancy_salary.append(f"От {vacs['salary']['from']} {vacs['salary']['currency']}")
                    # self.vacancy_salary.append(f"От {vacs['salary']} ")
                except TypeError:
                    try:
                        self.vacancy_salary.append(f"До {vacs['salary']['from']} {vacs['salary']['currency']}")
                    except TypeError:
                        self.vacancy_salary.append(f'Зарплата не указана')

                self.vacancy_urls.append(vacs['alternate_url'])
                self.vacancy_desc.append(vacs['snippet']['responsibility'])

    def information_output(self, next=-1):
        return f'Вакансия: {self.vacancy_names[next]}\n' \
               f'Описание: {self.vacancy_desc[next]}\n' \
               f'Заработная плата: {self.vacancy_salary[next]}\n' \
               f'Ссылка на вакансию: {self.vacancy_urls[next]}'





class AllErrors(Exception):
    """
    Класс включающий в себя классы ошибок
    """
    class ApiKeyError(Exception):
        """
        Ошибка ввода ключа
        """
        def __init__(self, api_key):
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
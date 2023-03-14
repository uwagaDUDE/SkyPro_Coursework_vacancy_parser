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
        parametres = {'per_page':v_count,
                      'page':v_page,
                      }

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
            print('Ошибка подключения, поиск вакансий в кэше...')

            try:
                with open('./.cache/HHru/vacancy_list.json', 'r', encoding='UTF-8') as hh:
                    pass
                    #TODO ДОДЕЛАТЬ РАБОТУ С КЭШЕМ

            except Exception:
                raise AllErrors().CacheError()

class SuperJob(SearchedVacancy):
    """
    Класс обработки получаемой информации с сайта superjob.ru
    """
    def __init__(self, vacancy_name):
        super().__init__(vacancy_name)
        api_key = script.api_loader()
        headers = {
            "X-Api-App-Id": api_key,
        }
        params = {
            "keyword": f"{vacancy_name}"
        }
        self.vacancy_list = requests.get(f'https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
        if self.vacancy_list.status_code == 200:

            with open('./.cache/Superjob/vacancy_list.json', 'w', encoding='UTF-8') as sj:
                vacancy_json = self.vacancy_list.json()
                sj.write(json.dumps(vacancy_json, indent=2, ensure_ascii=False))

        else:
            print('Ошибка подключения, поиск вакансий в кэше...')

            try:
                with open('./.cache/Superjob/vacancy_list.json', 'r', encoding='UTF-8') as sj:
                    pass
                    # TODO ДОДЕЛАТЬ РАБОТУ С КЭШЕМ

            except Exception:
                raise AllErrors().CacheError()


class GetVacancy(HeadHunterParse, SuperJob, VacancyCache):

    def __init__(self, vacancy_name):
        super().__init__(vacancy_name)
        super(HeadHunterParse, self).__init__(vacancy_name)
        super(SuperJob, self).__init__(vacancy_name)

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

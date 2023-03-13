import os
import requests
import json
from dotenv import load_dotenv as api
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

class HeadHunterParse:

    def __init__(self, vacancy_name='', v_count=10, v_page=1):
        """
        :param v_count: Количество вакансий, не более 20 на 1 странице!.
        :param v_page: Количество страниц, на 1 странице не более 20 вакансий.
        """
        parametres = {'per_page':v_count,
                      'page':v_page,
                      }
        self.vacancy_list = requests.get(f'https://api.hh.ru/vacancies?text={vacancy_name}&area=1&search_field=name', parametres)
        with open('./.cache/HHru/vacancy_list.json', 'w', encoding='UTF-8') as hh:
            vacancy_json = self.vacancy_list.json()
            hh.write(json.dumps(vacancy_json, indent=2, ensure_ascii=False))
            hh.close()



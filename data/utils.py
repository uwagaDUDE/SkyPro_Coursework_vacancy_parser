import requests
import json
from data import errors as Error
import psycopg2 as pg


def db_vacancy_search(password, vacancy_list):
    """
    :param password: Пароль к ДБ
    :param vacancy_list: JSON словарь, содержащий в себе вакансии
    Данная функция вносит вакансии из vacancy_list в таблицу founded_vacancy
    """
    with pg.connect(f'dbname=vacancy user=postgres host=localhost password={password}') as conn:
        with conn.cursor() as cur:

            try:
                for item in vacancy_list['items']:
                    if "salary" in item and item["salary"] \
                            is not None and "from" in item["salary"]\
                            and item["salary"]["from"] is not None:
                        anti_none_from = item["salary"]["from"]
                    else:
                        anti_none_from = 0

                    if "salary" in item and item["salary"]\
                            is not None and "to" in item["salary"]\
                            and item["salary"]["to"] is not None:
                        anti_none_to = item["salary"]["to"]
                    else:
                        anti_none_to = 0

                    if "salary" in item and item["salary"] is not None and "currency" in item["salary"] and item["salary"][
                            "currency"] is not None:
                            anti_none = item["salary"]["currency"]
                    else:
                        anti_none = 'Не указано'

                    cur.execute(f'INSERT INTO founded_vacancy (id, employeer_name, vacancy_name, vacancy_description,'
                                f'vacancy_salary_max, vacancy_salary_min, vacancy_salary_cur, '
                                f'vacancy_url) '
                                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
                                f'ON CONFLICT (id) DO UPDATE SET '
                                f'employeer_name = EXCLUDED.employeer_name, '
                                f'vacancy_name = EXCLUDED.vacancy_name, '
                                f'vacancy_description = EXCLUDED.vacancy_description, '
                                f'vacancy_salary_max = EXCLUDED.vacancy_salary_max, '
                                f'vacancy_salary_min = EXCLUDED.vacancy_salary_min, '
                                f'vacancy_salary_cur = EXCLUDED.vacancy_salary_cur, '
                                f'vacancy_url = EXCLUDED.vacancy_url',
                                (item['id'], item['employer']['name'], item["name"], item['snippet']['responsibility'],
                                anti_none_to, anti_none_from,
                                anti_none, item['alternate_url']))

            except Exception:
                for vac in vacancy_list['objects']:
                    print('Добавили что то с ')
                    cur.execute(f'INSERT INTO founded_vacancy (id, employeer_name, vacancy_name, vacancy_description,'
                                f'vacancy_salary_max, vacancy_salary_min, vacancy_salary_cur, '
                                f'vacancy_url) '
                                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
                                f'ON CONFLICT (id) DO UPDATE SET '
                                f'employeer_name = EXCLUDED.employeer_name, '
                                f'vacancy_name = EXCLUDED.vacancy_name, '
                                f'vacancy_description = EXCLUDED.vacancy_description, '
                                f'vacancy_salary_max = EXCLUDED.vacancy_salary_max, '
                                f'vacancy_salary_min = EXCLUDED.vacancy_salary_min, '
                                f'vacancy_salary_cur = EXCLUDED.vacancy_salary_cur, '
                                f'vacancy_url = EXCLUDED.vacancy_url',
                                (vac['id'], vac['firm_name'], vac['profession'], vac["candidat"],
                                 vac["payment_to"], vac["payment_from"],
                                 vac["currency"], vac["link"]))
def db_vacancy_output(password):
    with pg.connect(f'dbname=vacancy user=postgres host=localhost password={password}') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT vacancy_name, vacancy_description, vacancy_salary_min, vacancy_salary_max, "
                "vacancy_salary_cur, vacancy_url, employeer_name FROM founded_vacancy")

            # Получение результатов запроса
            rows = cur.fetchall()

            # Вывод информации о вакансиях
            for row in rows:
                print(f'Вакансия: {row[0]}\n'
                      f'Описание: {row[1]}\n'
                      f'Зарплата: от {row[2]} до {row[3]} {row[4]}\n'
                      f'Ссылка: {row[5]}\n'
                      f'Работодатель: {row[6]}\n')
                input(f'"ENTER" чтобы продолжить... ')


def api_loader():
    """
    Загружаем api_key с сайта, чтобы он не светился в коде
    :return:
    """
    try:
        api = requests.get('https://pastebin.com/raw/rFkMN0Xt') #'https://pastebin.com/raw/rFkMN0Xt'
        api_key = api.json()['key']
        return api_key
    except Exception:
        api_key = None
        raise Error.ApiKeyError(api_key)


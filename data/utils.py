import requests
import json
from data import errors as Error
import psycopg2 as pg


def db_vacancy_search(password, vacancy_list):
    with pg.connect(f'dbname=vacancy user=postgres host=localhost password={password}') as conn:
        with conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE founded_vacancy') # Чистим БД
            for item in vacancy_list['items']:
                if "salary" in item and item["salary"] is not None and "from" in item["salary"] and item["salary"][
                    "from"] is not None:
                    anti_none_from = item["salary"]["from"]
                else:
                    anti_none_from = 0

                if "salary" in item and item["salary"] is not None and "to" in item["salary"] and item["salary"][
                    "to"] is not None:
                    anti_none_to = item["salary"]["to"]
                else:
                    anti_none_to = 0

                if "salary" in item and item["salary"] is not None and "currency" in item["salary"] and item["salary"][
                    "currency"] is not None:
                    anti_none = item["salary"]['currency']
                else:
                    anti_none = 'Не указано'
                cur.execute(f'INSERT INTO founded_vacancy (id, employeer_name, vacancy_name, vacancy_description,'
                                f'vacancy_salary_max, vacancy_salary_min, vacancy_salary_cur, '
                                f'vacancy_url) '
                                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ',
                                (item['id'],item['employer']['name'], item["name"], item['snippet']['responsibility'],
                                 anti_none_to, anti_none_from,
                                 anti_none, item['alternate_url']))

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


def original_dict(cl, name, desc, v_f, v_c, v_t, v_u, v_id, v_emp):
    """
    :param cl: Название класса работы с вакансиями, в нашем случае - Vacancy
    :param name: Название вакансии
    :param desc: Описание вакансии
    :param v_f: Зарплата ОТ
    :param v_c: Зарплата валюта
    :param v_t: Зарплата ДО
    :param v_u: Ссылка на вакансию
    :param v_id: ID вакансии, предоставляемое сайтом
    :param v_emp: Работодатель
    :return:
    """
    vacancy_filter = set()
    try:
        for i in cl.vacancy_dict['items']:
            vacancy_filter.add((i['vacancy_name'], i['vacancy_emp']))
        if (name, v_emp) in vacancy_filter:
            pass
        else:
            cl.vacancy_list.append({
                    'my_id':cl.num_id,
                    'self_id':int(v_id),
                    'vacancy_name': name,
                    'vacancy_description': desc,
                    'vacancy_salary': {'from': v_f,
                                       'to': v_t,
                                       'cur': v_c},
                    'vacancy_url': v_u,
                    'vacancy_emp': v_emp
                     })
            cl.num_id = cl.num_id+1
            return cl
    except KeyError:
        cl.vacancy_list.append({
            'my_id': cl.num_id,
            'self_id': v_id,
            'vacancy_name': name,
            'vacancy_description': desc,
            'vacancy_salary': {'from': v_f,
                               'to': v_t,
                               'cur': v_c},
            'vacancy_url': v_u,
            'vacancy_emp': v_emp
        })
        cl.num_id = cl.num_id + 1
        return cl


def package(vacancy_list, cl):
    """
    Упаковка получаемого словаря с кучей информации в удобный словарь с нужной для работы инфой.
    :param vacancy_list: GET-Атрибут
    :param cl: Класс вакансий (Vacancy)
    :return:
    """
    try:
        for vac in vacancy_list['items']:
            v_id = vac['id']
            v_name = vac['name']
            if vac['snippet']['responsibility'] == None:
                v_desc = 'Описание не указано'
            else:
                v_desc = vac['snippet']['responsibility']
            v_url = vac['alternate_url']
            v_emp = vac['employer']['name']
            try:
                if vac['salary']['from'] == None:
                    v_salary_from = 0
                else:
                    v_salary_from = vac['salary']['from']
                if vac['salary']['to'] == None:
                    v_salary_to = 'не указано'
                else:
                    v_salary_to = vac['salary']['to']
                v_salary_cur = vac['salary']['currency']
            except TypeError:
                v_salary_from = 'не указано'
                v_salary_to = 'не указано'
                v_salary_cur = ''
            original_dict(cl, v_name, v_desc, v_salary_from,
                          v_salary_cur, v_salary_to, v_url, v_id, v_emp)

    except KeyError:
        for vac in vacancy_list['objects']:
            v_name = vac['profession']
            v_id = vac['id']
            v_desc = vac["candidat"]
            v_salary_from = vac["payment_from"]
            v_salary_to = vac["payment_to"]
            v_salary_cur = vac["currency"]
            v_emp = vac['firm_name']
            try:
                v_url = vac["link"]
            except KeyError:
                v_url = ('не рабочая ссылка :(')
            original_dict(cl, v_name, v_desc, v_salary_from,
                          v_salary_cur, v_salary_to, v_url, v_id, v_emp)
    with open('./.cache.json', 'w', encoding='UTF-8') as file:
        cl.vacancy_dict['items'] = cl.vacancy_list
        wrt = json.dumps(cl.vacancy_dict, indent=2, ensure_ascii=False)
        file.write(wrt)


def liked_proffesion(user_like, cl):
    """
    Проверка, понравилась ли последняя вакансия пользователю
    :param user_like: ответ пользователя
    :return:
    """
    yes_answers = ['да', "+", "=", 'lf', 'da', 'yes',
                   'нуы', 'ДА', 'Да', 'дА', 'Lf', 'Yes',
                   'yEs', 'YEs', 'YES', 'yES', 'yeS', 'YeS',
                   'lF', 'LF']
    if user_like.lower() in yes_answers:
        try:
            with open('./last_search.json', "r", encoding='UTF-8') as last:
                last_load = json.load(last)
                cl.like_id.append(last_load['self_id'])
                with open('./liked_vacancy.json', "a", encoding='UTF-8') as liked:
                    liked.write(f"{last_load['vacancy_name']}:{last_load['vacancy_url']}\n")
                    return f'Ищем дальше :)'
        except Exception:
            raise Error.UnavalibleLike()


def usd_converter():
    usd_get = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    valute_dict = usd_get.json()
    usd_price = valute_dict['Valute']['USD']['Value']
    return int(usd_price)


def max_salary():
    """
    Выводит вакансию с максимальной заработной платой, с учетом конвертации из долларов в рубли.
    :return: Вакансия с максимальной ЗП
    """
    sal_list = []
    sal_list_ids = []
    with open('./.cache.json', "r", encoding='UTF-8') as max_salary:
        json_dict = json.load(max_salary)
        for item in json_dict['items']:
            if item["vacancy_salary"]['to'] == 'не указано' or item["vacancy_salary"]['to'] == 0:
                pass
            else:
                max_sal = item["vacancy_salary"]['to']
                max_sal_id = item["self_id"]
                if item['vacancy_salary']['cur'] == 'USD':
                    try:
                        max_sal = item["vacancy_salary"]['to']*usd_converter()
                    except Exception:
                        max_sal = item["vacancy_salary"]['from']*usd_converter()

                sal_list_ids.append(max_sal_id)
                sal_list.append(max_sal)
        x = max(sal_list)
        y = sal_list.index(x)
        for sal in json_dict['items']:
            if sal_list_ids[y] == sal['self_id']:
                return f'Вакансия: {sal["vacancy_name"]}\n' \
                   f'Описание: {sal["vacancy_description"]}\n' \
                   f'Зарплата: от {sal["vacancy_salary"]["from"]} ' \
                   f'до {sal["vacancy_salary"]["to"]} {sal["vacancy_salary"]["cur"]}\n' \
                   f'Ссылка: {sal["vacancy_url"]}\n' \
                   f'Работодатель: {sal["vacancy_emp"]}'


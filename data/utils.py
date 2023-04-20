import requests
import json
from data import errors as Error

def db_input(cur, name, desc, v_f, v_c, v_t, v_u, lines):
    counter = lines+1
    cur.execute(f'INSERT INTO founded_vacancy '
                f'({counter}, {name}, {desc}, {v_f}, {v_t}, {v_c}, {v_u})')
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


def original_dict(cl, name, desc, v_f, v_c, v_t, v_u, v_id, v_emp, cur):
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
                    'self_id':v_id,
                    'vacancy_name': name,
                    'vacancy_description': desc,
                    'vacancy_salary': {'from': v_f,
                                       'to': v_t,
                                       'cur': v_c},
                    'vacancy_url': v_u,
                    'vacancy_emp': v_emp
                     })
            cl.num_id = cl.num_id+1
            db_input(cur, name, desc, v_f, v_c, v_t, v_u, cl.num_id)
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
        db_input(cur, name, desc, v_f, v_c, v_t, v_u, cl.num_id)
        return cl


def package(vacancy_list, cl, cur):
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
                          v_salary_cur, v_salary_to, v_url, v_id, v_emp, cur)

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
                          v_salary_cur, v_salary_to, v_url, v_id, v_emp, cur)
    with open('../.cache.json', 'w', encoding='UTF-8') as file:
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
            with open('../last_search.json', "r", encoding='UTF-8') as last:
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
    with open('../.cache.json', "r", encoding='UTF-8') as max_salary:
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


if __name__ == '__main__':  # Для тестовых запусков
    print(max_salary())

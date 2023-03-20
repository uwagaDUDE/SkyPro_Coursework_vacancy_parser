import requests
import classes as cl
import json


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
        raise cl.AllErrors().ApiKeyError(api_key)


def original_dict(cl, name, desc, v_f, v_c, v_t, v_u):
    cl.vacancy_list.append({
        'id':cl.num_id,
        'vacancy_name': name,
        'vacancy_description': desc,
        'vacancy_salary': {'from': v_f,
                           'to': v_t,
                           'cur': v_c},
        'vacancy_url': v_u
         })
    cl.num_id = cl.num_id+1
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
            v_name = vac['name']
            v_desc = vac['snippet']['responsibility']
            v_url = vac['alternate_url']
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
            original_dict(cl, v_name, v_desc, v_salary_from, v_salary_cur, v_salary_to, v_url)

    except KeyError:
        for vac in vacancy_list['objects']:
            v_name = vac['profession']
            v_desc = vac["candidat"]
            v_salary_from = vac["payment_from"]
            v_salary_to = vac["payment_to"]
            v_salary_cur = vac["currency"]
            try:
                v_url = vac["link"]
            except KeyError:
                v_url = ('не рабочая ссылка :(')
            original_dict(cl, v_name, v_desc, v_salary_from, v_salary_cur, v_salary_to, v_url)
    with open('./.cache.json', 'w', encoding='UTF-8') as file:
        cl.vacancy_dict['items'] = cl.vacancy_list
        wrt = json.dumps(cl.vacancy_dict, indent=2, ensure_ascii=False)
        file.write(wrt)


def liked_proffesion(user_like):
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
            with open('last_search.json', "r", encoding='UTF-8') as last:
                last_load = json.load(last)
                with open('./liked_vacancy.txt', "a", encoding='UTF-8') as liked:
                    liked.write(f"{last_load['vacancy_name']}:{last_load['vacancy_url']}\n")
                    return ('Ищем дальше :)')
        except Exception:
            print('Error')
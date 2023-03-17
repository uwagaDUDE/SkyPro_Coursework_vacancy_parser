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

def check_str(hh_attribute):
    """
    Проверка на то, является ли атрибут числом
    :param hh_attribute: атрибут отвечающий за количество вакансий/страниц
    :return: атрибут
    """
    if hh_attribute.isnumeric():
        return hh_attribute
    else:
        raise cl.AllErrors().WrongInput()


def check_max_len(hh_pages, hh_vacs):
    """
    Проверка максимальной длинны поиска
    :param hh_pages: количество страниц
    :param hh_vacs: количество вакансий
    :return:
    """
    if int(hh_vacs) > 100:
        raise cl.AllErrors().WrongMaxValue()
    elif int(hh_pages)*int(hh_vacs) > 2000:
        raise cl.AllErrors().WrongMaxVacancies()
    else:
        pass


def open_file(folder, request):
    """
    Функция которая записывает в файл информацию о вакансиях
    :param folder: Папка в .cache хранящая в себе информацию с вакансиями (HHru, Superjob)
    :param request: Атрибут содрежащий get запрос
    :return:
    """
    try:
        with open(f'./.cache/{folder}/vacancy_list.json', 'w', encoding='UTF-8') as vc_file:
            vacancy_json = request.json()
            vc_file.write(json.dumps(vacancy_json, indent=2, ensure_ascii=False))
    except Exception as Error:
        print(f'Произошла ошибка:'
              f'{Error}')

def get_vacancy_information(file, v_name, v_desc, v_url, v_salary_from, v_salary_to, v_salary_cur):
    """
    :param file: Атрибут файла
    :param v_name: Атрибут списка содержащий названия вакансий
    :param v_salary_from: Атрбиут зп ОТ
    :param v_salary_to: Атрибут зп ДО
    :param v_desc: Атрибут описания вакансии
    :param v_url: Атрибут ссылки на вакансию
    :param v_salary_cur: Атрибут валюты
    :return:
    """
    try:
        for vac in file['items']:
            v_name.append(vac['name'])
            v_desc.append(vac['snippet']['responsibility'])
            v_url.append(vac['alternate_url'])
            try:
                if vac['salary']['from'] == None:
                    v_salary_from.append('0')
                else:
                    v_salary_from.append(vac['salary']['from'])
                if vac['salary']['to'] == None:
                    v_salary_to.append('не указано')
                else:
                    v_salary_to.append(vac['salary']['to'])
                v_salary_cur.append(vac['salary']['currency'])
            except TypeError:
                v_salary_from.append('не указано')
                v_salary_to.append('не указано')
                v_salary_cur.append('')

    except KeyError:
        for vac in file['objects']:
            v_name.append(vac['profession'])
            v_desc.append(vac["candidat"])
            v_url.append(vac["client"]["link"])
            v_salary_from.append(vac["payment_from"])
            v_salary_to.append(vac["payment_to"])
            v_salary_cur.append(vac["currency"])


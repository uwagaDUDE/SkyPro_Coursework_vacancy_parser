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
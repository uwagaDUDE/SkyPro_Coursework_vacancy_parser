import requests
import classes as cl

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
    if int(hh_vacs) > 20:
        raise cl.AllErrors().WrongMaxValue()
    elif int(hh_pages)*int(hh_vacs) > 2000:
        raise cl.AllErrors().WrongMaxVacancies()
    else:
        pass
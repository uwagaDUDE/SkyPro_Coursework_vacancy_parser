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

def get_vacancy_information(file, names, salary_f, salary_t, desc, urls, cur):
    """
    :param file: Атрибут файла
    :param names: Атрибут списка содержащий названия вакансий
    :param salary_f: Атрбиут зп ОТ
    :param salary_t: Атрибут зп ДО
    :param desc: Атрибут описания вакансии
    :param urls: Атрибут ссылки на вакансию
    :param cur: Атрибут валюты
    :return:
    """

    for vac in file.get('items', 'objects'):
        if 'name' in vac:
            print(vac)
            names.append(vac.get('name'))
        else:
            names.append(file['objects'][0]['profession'])

        try:
            salary_from = vac['salary'].get('from')
            salary_to = vac['salary'].get('to')

        except AttributeError:
            try:
                salary_from = file['objects'][0]['payment_from']
                salary_to = file['objects'][0]['payment_to']

            except KeyError:
                salary_from, salary_to = 'Не указано', 'Не указано'

        except TypeError:
            try:
                salary_from = file['objects'][0]['payment_from']
                salary_to = file['objects'][0]['payment_to']

            except KeyError:
                salary_from, salary_to = 'Не указано', 'Не указано'

        salary_f.append(salary_from)
        salary_t.append(salary_to)
        try:
            salary_cur = vac['salary'].get('currency', '-')
            cur.append(salary_cur)

        except TypeError:
            try:
                salary_cur = file['objects'][0]['currency']
                cur.append(salary_cur)

            except KeyError:
                salary_cur = ''
                cur.append(salary_cur)

        except AttributeError:
            try:
                salary_cur = file['objects'][0]['currency']
                cur.append(salary_cur)

            except KeyError:
                salary_cur = ''
                cur.append(salary_cur)

        if "alternate_url" in vac:
            urls.append(vac.get('alternate_url', 'client'))
            responsibility = vac['snippet']['responsibility']

        else:
            try:
                urls.append(file['objects'][0]['client']['link'])
                responsibility = file['objects'][0]['client']['description']

            except KeyError:
                urls.append('Ошибка')
                responsibility = file['objects'][0]['client']['description']
        desc.append(responsibility)
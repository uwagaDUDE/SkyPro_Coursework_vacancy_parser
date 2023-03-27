class ApiKeyError(Exception):
    """
    Ошибка ввода ключа
    """
    def __init__(self, api_key):
        """
        :param api_key: API ключ
        """
        if api_key == None:
            raise Exception(f'Ошибка ввода ключа, попробуйте ввести его вручную.')


class CacheError(Exception):
    def __init__(self):
        raise Exception(f'Файла с кэшом не найдено.')


class WrongInput(Exception):
    def __init__(self):
        raise Exception(f'Ошибка ввода! Вводите только цифры!')


class WrongMaxValue(Exception):
    def __init__(self):
        raise Exception(f'Вакансий должно быть не больше 20 на 1 странице!')


class WrongMaxVacancies(Exception):
    def __init__(self):
        raise Exception(f'Всего количество вакансий не должно превышать 2000!')


class UnknowVacancie(Exception):
    def __init__(self):
        raise Exception(f'Такой вакансии не найдено.')


class UnavalibleLike(Exception):
    def __init__(self):
        raise Exception(f'Невозможно сохранить вакансию!')
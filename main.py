from data import utils as functions, classes as scripts
import os
from dotenv import dotenv_values
cycle = True



if __name__ == '__main__':

    try:
        password = dotenv_values('.env')['PASSWORD']
    except Exception as AllErrors:
        env_file = open('.env', 'w', encoding="UTF-8")
        print('Введите пароль к базе данных!')
        password = input('Password: ')
        env_file.write(f'PASSWORD={password}')
        env_file.close()
        password = dotenv_values('.env')['PASSWORD']

    db = scripts.DataBase(password)

    while True:

        print('  ### МЕНЮ ### ')
        print('Что будем искать?\n'
              '1. Работодателя\n'
              '2. Вакансию\n'
              '3. Средняя ЗП по всем вакансиям')
        user_answer = input('Ваш выбор: ')

        if user_answer == '2':

            vc_searched = input(f'Введите название искомой вакансии: ')
            scripts.Vacancy(vc_searched).start(password)  # Инициализация программы

            while cycle is not False:

                vacancy = scripts.Vacancy(vc_searched)
                print(f'\n{vacancy}')
                print('"stop" чтобы закончить поиск вакансий')
                user_like = input(f'"ENTER" чтобы продолжить: ')

                if user_like.lower() == 'stop':
                    cycle = False
                    print('Надеюсь вы нашли что искали :)')

        elif user_answer == '1':

            print('  ### МЕНЮ ### ')
            print('1. Поиск по имени работодателя')
            print('2. Сколько всего вакансий от работодателя у нас в базе данных')
            print('3. Поиск вакансий у работодателя по ключевому слову\n'
                  '4. Поиск вакансий у которых зарплата выше средней')
            user_choose = input('Ваш выбор: ')
            if user_choose == '1':
                emp_search = input('Работодатель: ')
                db.get_urls(emp_search)
                db.get_vacancy(password)
                db.get_employeer(password, emp_search)
            elif user_choose == '2':
                db.get_all_vacancies(password)
            elif user_choose == "4":
                key_word = input('Введите ключевое слово: ')
                db.get_vacancies_with_keyword(password, key_word)
            elif user_choose == '5':
                db.get_max_avg(password)

        elif user_answer == '3':
            print(db.get_avg_salary(password))

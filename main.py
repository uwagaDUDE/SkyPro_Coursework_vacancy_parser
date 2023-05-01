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
        print('Что будем делать?\n'
              '1. Искать вакансию\n'
              '2. Фильтр по работодателю\n'
              '3. Средняя ЗП по всем вакансиям\n'
              '4. Поиск вакансий по зарплате, которая выше средней\n'
              '5. Сколько всего вакансий работодателя\n'
              '6. Поиск всех вакансий по имени работодателя')
        user_answer = input('Ваш выбор: ')

        if user_answer == '1':

            vc_searched = input(f'Введите название искомой вакансии: ')
            scripts.Vacancy(vc_searched).start(password)  # Инициализация программы

            while cycle is not False:

                scripts.Vacancy(vc_searched)
                functions.db_vacancy_output(password, vc_searched)

        elif user_answer == '2':

            print('  ### МЕНЮ ### ')
            print('1. Внести работодателя в базу данных')
            print('2. Поиск вакансий у работодателя по ключевому слову')

            user_choose = input('Ваш выбор: ')

            if user_choose == '1':
                emp_search = input('Работодатель: ')
                db.get_urls(emp_search)
                db.get_vacancy(password)
                db.get_employeer(password, emp_search)

            elif user_choose == "2":
                key_word = input('Введите ключевое слово: ')
                employer = input('Название работодателя: ')
                db.get_vacancies_with_keyword(password, key_word, employer)

        elif user_answer == '3':
            print(db.get_avg_salary(password))

        elif user_answer == '4':
            print(db.get_max_avg(password))

        elif user_answer == '5':
            db.get_companies_and_vacancies_count(password)

        elif user_answer == "6":
            emp = input('Имя работодателя: ')
            db.get_emp_vacancies(password, emp)
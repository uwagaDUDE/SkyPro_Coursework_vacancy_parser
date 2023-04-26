from data import utils as functions, classes as scripts
import os
cycle = True

if __name__ == '__main__':
    while True:
        print('  ### МЕНЮ ### ')
        print('Что будем искать?\n'
              '1. Работодателя\n'
              '2. Вакансию')
        user_answer = input('Ваш выбор: ')
        if user_answer == 2:
            vc_searched = input(f'Введите название искомой вакансии: ')
            scripts.Vacancy(vc_searched).start()  # Инициализация программы

            while cycle is not False:

                vacancy = scripts.Vacancy(vc_searched)
                print(f'\n{vacancy}')
                print('\nПонравилась вакансия?')
                user_like = input(f'(Да/нет/stop/max): ')

                if user_like.lower() == 'stop':
                    cycle = False
                    print('Надеюсь вы нашли что искали :)')

                if user_like.lower() == 'max':
                    print(functions.max_salary())
                    input('Нажмите ENTER чтобы продолжить')

                functions.liked_proffesion(user_like, vacancy)
        elif user_answer == 1:
            print('  ### МЕНЮ ### ')
            print('1. Поиск по имени работодателя')
            print('2. Сколько всего вакансий от работодателя у нас в базе данных')
            print('3. Средняя зарплата по всем вакансиям')
            print('4. Поиск вакансий у работодателя по ключевому слову\n'
                  '5. Поиск вакансий у которых зарплата выше средней')
            user_choose = input('Ваш выбор: ')
            if user_choose == 1:


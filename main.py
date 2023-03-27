from data import utils as functions, classes as scripts

cycle = True
if __name__ == '__main__':
    vc_searched = input(f'Введите название искомой вакансии: ')
    scripts.Vacancy(vc_searched).start()  # Инициализация программы
    while cycle != False:
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
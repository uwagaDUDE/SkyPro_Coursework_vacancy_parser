import classes as scripts
import utils as functions

cycle = True
if __name__ == '__main__':
    vc_searched = input(f'Введите название искомой вакансии: ')
    scripts.Vacancy(vc_searched).start()
    while cycle != False:
        vacancy = scripts.Vacancy(vc_searched)
        print(f'\n{vacancy}')
        print('\nПонравилась вакансия?')
        user_like = input(f'(Да/нет/stop/max): ')
        if user_like.lower() == 'stop':
            cycle = False
            print('Надеюсь вы нашли что искали :)')
        elif user_like.lower() == 'max':  # Не работает на данный момент
            functions.max_salary()
        functions.liked_proffesion(user_like, vacancy)
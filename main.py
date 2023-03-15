import classes as scripts
import utils as functions

if __name__ == '__main__':
    vc_searched = input(f'Введите название искомой вакансии: ')
    hh_vc_counter = input(f'Введите количество вакансий на странице (не более 100): ')
    hh_pages = input(f'Страницу начала поиска: ')
    functions.check_str(hh_vc_counter), functions.check_str(hh_pages), functions.check_max_len(hh_pages, hh_vc_counter)
    # vacancy = scripts.GetVacancy(vc_searched, hh_vc_counter, hh_pages)

    vacancy = scripts.GetVacancy(vc_searched, hh_vc_counter, hh_pages)
    vacancy.get_hh()
    search_cycle = True
    vacancy.vacancy_package()
    next = 0
    # x = (max(vacancy.vacancy_salary))
    # y = vacancy.vacancy_salary.index(x)
    while search_cycle != False:

        if next > len(vacancy.vacancy_names):
            search_cycle = False
            break
        search = input(f'Ищем дальше(+/-): ')
        if search == '+':
            print(vacancy)

        elif search == '-':
            search_cycle = False
            print(f'Надеюсь вы нашли что искали :)')
        else:
            print('Введите + либо -')


import classes as scripts
import utils as functions

if __name__ == '__main__':
    # vc_searched = input(f'Введите название искомой вакансии: ')
    # hh_vc_counter = input(f'Введите количество вакансий на странице (не более 20): ')
    # hh_pages = input(f'Введите количество страниц для поиска: ')
    # functions.check_str(hh_vc_counter), functions.check_str(hh_pages), functions.check_max_len(hh_pages, hh_vc_counter)
    vacancy = scripts.GetVacancy('python', 10, 1)
    vacancy.get_hh()
    search_cycle = True
    next = 0
    print(vacancy.information_output(next))
    while search_cycle != False:
        next = next+1
        search = input(f'Ищем дальше(+/-): ')
        if search == '+':
            print(vacancy.information_output(next))
        elif search == '-':
            search_cycle = False
        else:
            print('Введите + либо -')


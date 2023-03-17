import classes as scripts
import utils as functions

if __name__ == '__main__':
    vc_searched = input(f'Введите название искомой вакансии: ')
    hh_vc_counter = input(f'Введите количество вакансий на странице (не более 100): ')
    hh_pages = input(f'Страницу начала поиска: ')
    functions.check_str(hh_vc_counter), functions.check_str(hh_pages), functions.check_max_len(hh_pages, hh_vc_counter)
    # vacancy = scripts.GetVacancy(vc_searched, hh_vc_counter, hh_pages)

    vacancy = scripts.GetVacancy(vc_searched, hh_vc_counter, hh_pages)
    vacancy.parse()
    search_cycle = True
    vacancy.vacancy_package()
    next = 0
    # x = (max(vacancy.vacancy_salary))
    # y = vacancy.vacancy_salary.index(x)
    with open('liked_vacancy.txt', 'r+', encoding='UTF-8') as tinder:

        while search_cycle != False:

            if next > len(vacancy.vacancy_names):
                search_cycle = False
                break
            next = next+1
            print(vacancy)
            search = input(f'Понравилась вакансия(+/-): ')
            if search == '+':
                tinder.writelines(f'{vacancy.vacancy_urls[next-1]}\n') #TODO Доделать механнику как в Tinder

            elif search == '-':
                print(f'Ищем дальше :)')
            else:
                print('Введите + либо -')


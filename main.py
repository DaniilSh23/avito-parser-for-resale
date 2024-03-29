import time
from avarage_price_calculation import product_data_processing
from get_page_numbers import get_page_numbers
from parse_products import parse_products


def main():
    start = time.time()
    url = input('Введите url адрес: ')
    numb_of_pages = get_page_numbers(url)
    print('============================'
        f'\nНайдено {numb_of_pages} страниц с товарами\n'
        f'Приступаю к сбору информации на страницах\n'
          '============================')
    parse_products(numb_of_pages, url)
    print('============================'
          '\nПервый шаг парсинга выполнен.'
          '\nРезультат в файле fst_step_parse.csv\n'
          'Приступаю к поиску средней цены\n'
          '============================')
    print(f'Время выполнения первого шага: {time.time() - start}')
    start = time.time()
    product_data_processing()
    print('============================'
          '\nИнформация успешно собрана.'
          '\nРезультат в файле sec_step_parse.csv\n'
          '============================')
    print(f'Время выполнения второго шага: {time.time() - start}')


if __name__ == '__main__':
    main()

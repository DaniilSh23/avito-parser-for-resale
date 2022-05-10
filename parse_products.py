import csv
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import pandas as pd


def parse_products(numb_of_pages: int, url: str) -> None:
    '''
    Функция для сбора информации о товарах.
    Записывает JSON файл, как результат своей работы.

    :param numb_of_pages: число страниц с товарами
    :param url: адрес запроса
    :return: None
    '''

    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent.random}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(
        executable_path=r'.\chromedriver\chromedriver.exe',
        options=options,
    )

    stealth(
        driver,
        languages=['ru-ru', 'ru'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        render='Intel Iris OpenGL Engine',
        fix_hairline=True,
    )

    try:
        # переменные, необходимые для парсинга
        product_title_cls = 'iva-item-titleStep-pdebR'
        product_price_cls = 'iva-item-priceStep-uq2CQ'
        publication_age_cls = 'iva-item-dateInfoStep-_acjp'
        product_link_cls = 'iva-item-sliderLink-uLz1v'

        # записываем заголовки данных в файл
        with open('fst_step_parse.csv', 'w', encoding='cp1251', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([
            'id',
            'Название товара',
            'Цена товара',
            'Давность публикации',
            'Ссылка на товар',
        ])

        # на каждой странице собираем объявления
        for i_page in range(1, numb_of_pages + 1):
            # в url запросе для движения по страницам может быть и параметр cd, вместо p
            page_url = '/'.join([url, f'?p={i_page}'])
            driver.get(page_url)
            time.sleep(0.5)
            product_list = driver.find_elements(by=By.CLASS_NAME, value='iva-item-content-rejJg')

            page_product_dct = {}
            data_frame = pd.DataFrame()
            for i_num, i_product in enumerate(product_list):
                # собираем информацию об объявлениях
                try:
                    i_product_price = i_product.find_element(by=By.CLASS_NAME, value=f'{product_price_cls}')
                    i_product_price = i_product_price.find_element(by=By.TAG_NAME, value='span')
                    i_product_price = i_product_price.find_element(by=By.TAG_NAME, value='span')
                    i_product_price = i_product_price.find_element(by=By.TAG_NAME, value='span').text.replace(' ',
                                                                                                              '').replace('₽', '')

                    i_product_title = i_product.find_element(by=By.CLASS_NAME, value=product_title_cls)
                    i_product_title = i_product_title.find_element(by=By.TAG_NAME, value='a')
                    i_product_title = i_product_title.find_element(by=By.TAG_NAME, value='h3').text

                    i_product_publ_age = i_product.find_element(by=By.CLASS_NAME, value=f'{publication_age_cls}')
                    i_product_publ_age = i_product_publ_age.find_element(by=By.TAG_NAME, value='div')
                    i_product_publ_age = i_product_publ_age.find_element(by=By.TAG_NAME, value='span')
                    i_product_publ_age = i_product_publ_age.find_element(by=By.TAG_NAME, value='span')
                    i_product_publ_age = i_product_publ_age.find_element(by=By.TAG_NAME, value='div').text

                    i_product_link = i_product.find_element(by=By.CLASS_NAME, value=product_link_cls).get_attribute(
                        'href')

                    # вносим значения в словарь для итерируемого товара
                    page_product_dct['id'] = ''.join([str(i_page), str(i_num)])
                    page_product_dct['Название товара'] = i_product_title
                    page_product_dct['Цена товара'] = i_product_price
                    page_product_dct['Давность публикации'] = i_product_publ_age
                    page_product_dct['Ссылка на товар'] = i_product_link

                    data_frame = data_frame.append(page_product_dct, ignore_index=True)
                except Exception as error:
                    print(f'На странице № {i_page} с товаром № {i_num} произошла проблема\n{error}')

            # устанавливаем колонку id, как индекс для DataFrame
            data_frame = data_frame.set_index('id')

            # записываем в таблицу данные итерируемого товара
            with open('fst_step_parse.csv', 'a', encoding='cp1251', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                for index, row in data_frame.iterrows():
                    list_to_write = [
                        index,
                        row['Название товара'],
                        row['Цена товара'],
                        row['Давность публикации'],
                        row['Ссылка на товар'],
                    ]
                    writer.writerow(list_to_write)
                print(f'Страница № {i_page}, записано в файл {data_frame.count()} товаров.\n')

    except Exception as error:
        print(f'Ошибка запроса: {error}')
    finally:
        driver.close()
        driver.quit()
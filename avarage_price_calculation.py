import csv
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import pandas as pd


def product_data_processing():
    '''
    Функция для поиска товаров по всей РФ и подсчёта среднерыночной (условно) цены
    :return None: как результат своей работы создаёт файл csv
    '''

    data_frame = pd.read_csv('fst_step_parse.csv', index_col='id', encoding='cp1251', sep=';')
    data_frame_for_processing = pd.DataFrame()

    for i_indx, i_row in data_frame.iterrows():
        print(f'Айдишник {i_indx}\n Строка {i_row["Название товара"]}')
        i_product_id = i_indx
        i_product_title = i_row["Название товара"]
        i_product_price = i_row["Цена товара"]

        # проверяем наличие в товаре цены
        if isinstance(i_product_price, int):
            splitted_title = i_product_title.split()
            title_for_url = '+'.join(splitted_title)
            url_for_func = ''.join(['https://www.avito.ru/rossiya?q=', title_for_url])
            avarage_market_price = req_for_avarage_price(url=url_for_func)
            price_ratio = price_ratio_calculation(avarage_market_price, float(i_product_price))

        else:
            avarage_market_price = 'Цена не указана'
            price_ratio = 'Цена не указана'
        # создаём словарь для записи новой строки в DataFrame
        new_row = {
            'id': i_product_id,
            'средняя цена товара': avarage_market_price,
            'девиация цен в %': price_ratio,
        }
        # добавляем запись в DataFrame
        data_frame_for_processing = data_frame_for_processing.append(new_row, ignore_index=True)
        print(f'===================================\n{data_frame_for_processing}')


    else:
        with open('sec_step_parse.csv', 'a', encoding='cp1251', newline='') as sec_file:
            # устанавливаем индексом значение id
            data_frame_for_processing = data_frame_for_processing.set_index('id')
            # запишем заголовки в файл
            writer = csv.writer(sec_file, delimiter=';')
            writer.writerow([
                'id',
                'Название товара',
                'Цена товара',
                'Давность публикации',
                'Ссылка на товар',
                'средняя цена товара',
                'девиация цен в %'
            ])
            # соединяем два DataFrame
            # joint_data_frame = pd.merge(data_frame, data_frame_for_processing, how='inner', left_index=True, right_on='id')
            joint_data_frame = pd.concat([data_frame, data_frame_for_processing], axis=1)
            # сортировка по убыванию по столбцу девиации цен
            sorted_joint_data_frame = joint_data_frame.sort_values(by='девиация цен в %')
            for i_indx, i_row in sorted_joint_data_frame.iterrows():
                list_to_write = [
                    i_indx,
                    i_row['Название товара'],
                    i_row['Цена товара'],
                    i_row['Давность публикации'],
                    i_row['Ссылка на товар'],
                    i_row['средняя цена товара'],
                    ''.join([str(i_row['девиация цен в %']), '%'])
                ]
                writer.writerow(list_to_write)


def req_for_avarage_price(url: str) -> float:
    '''
    Функция для выполнения запроса к сайту и расчёта средней цены товаров.
    :param url: адрес для выполнения запроса
    :return avarage_market_price: средняя цена
    '''

    # предварительные настройки для браузера
    user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent.random}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\1\OneDrive\Рабочий стол\Pet-проект\profitable-goods-parser-avito\avito-profitable-goods-parser\chromedriver\chromedriver.exe',
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
        # делаем запрос
        driver.get(url)
        time.sleep(0.5)

        # Собираем объявления со страницы
        product_list = driver.find_elements(by=By.CLASS_NAME, value='iva-item-content-rejJg')

        product_price_cls = 'iva-item-priceStep-uq2CQ'
        summ_prices = 0
        non_price_objects = 0

        # суммируем цены всех объявлений
        for i_num, i_product in enumerate(product_list):
            i_product_price = i_product.find_element(by=By.CLASS_NAME, value=f'{product_price_cls}')
            i_product_price = i_product_price.find_element(by=By.TAG_NAME, value='span')
            i_product_price = i_product_price.find_element(by=By.TAG_NAME, value='span')
            i_product_price = i_product_price.find_element(by=By.TAG_NAME, value='span').text.replace(' ', '').replace(
                '₽', '')

            # если цена в товаре не указана
            if not i_product_price.isdigit():
                # добавим значение, которое скорректируем потом наш расчёт средней цены
                non_price_objects += 1
                continue
            summ_prices += float(i_product_price)

        # считаем среднюю цену объявлений 1-й страницы
        avarage_market_price = summ_prices / (len(product_list) - non_price_objects)

    except Exception as error:
        print(f'При запросе для поиска средней цены произошла ошибка \n{error}')
    finally:
        driver.close()
        driver.quit()
        return round(avarage_market_price, 2)


def price_ratio_calculation(avarage_market_price: float, product_price: float) -> float:
    '''
    Расчёт отношения цены товарв и среднерыночной (условно) цены.
    :param avarage_market_price: среднерыночная (условно) цена
    :param product_price: цена товара
    :return: float
    '''

    result = (1 - product_price / avarage_market_price) * (-1) * 100
    return round(result, 2)


import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


def get_page_numbers(url: str) -> int:
    '''
    Функция для определения общего количества страниц с товарами.
    :param url: str - адрес запроса
    :return numb_of_pages: int - число страниц
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
        # делаем запрос
        driver.get(url)
        time.sleep(0.5)
        # берём число страниц с товарами и делаем его integer
        page_numb_list = driver.find_elements(by=By.CLASS_NAME, value='pagination-item-JJq_j')
        numb_of_pages = int(page_numb_list[len(page_numb_list) - 2].text)
    except Exception as error:
        print('При определении количества страниц с товарами произошла ошибка\n'
              f'{error}')
    finally:
        driver.close()
        driver.quit()
        return numb_of_pages
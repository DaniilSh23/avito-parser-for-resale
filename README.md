# Парсер авито для перепродажи товаров

## Язык программирования
* Python 3.10

## Используемые библиотеки
* pandas
* selenium
* csv
* time
* selenium_stealth

## Краткое описание принципа работы
* Данный скрипт получает на вход ссылку на авито, в следующем формате
```https://www.avito.ru/<регион поиска>/<категория товаров>```
* Далее определяет количество страниц с результатами
* Собирает на этих страницах информацию о товарах и сохраняет в файл fst_step_parse.csv
* Ищет условно среднерыночную цену (ниже поясню подробно как это реализовал я, Ваши идеи приветствуются)
* Формирует файл sec_step_parse.csv , в котором информация отсортирована в соответствии с девиацией цены от условно-среднерыночной

### Детальное описание
* Данный скрипт реализован с помощью библиотеки selenium, которая использует Ваш браузер для сбора информации с сайта. В связи с этим есть проблема в скорости работы данного скрипта, так как webdriver ждёт полной загрузки страницы, прежде чем начать выполнение дальнейшего кода.
* Причина использования именно selenium заключается в том, что Авито не охотно отдаёт информацию о товарах, собираемую путём автоматизации.
* Для работы скрипта необходим браузер Google Chrome, а также драйвер вашей версии браузера для библиотеки selenium.
* Для структурирования данных в табличном виде и записи в файл используется библиотека pandas, однако запись в csv файл реализовано классическим методом библиотеки csv, по причине разного рода проблем вызываемых при записи с применением библиотеки pandas. Это мой первый опыт использования pandas, поэтому буду рад обратной связи по улучшению скрипта. 
* Также в данном скрипте настроена кодировка для пользователей ОС Windows (cp1251), но вы всегда можете изменить её на (utf-8).



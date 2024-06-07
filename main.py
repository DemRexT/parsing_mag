from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
from bs4 import BeautifulSoup
import csv

driver = webdriver.Chrome(executable_path='C:\\Users\\danil\\PycharmProjects\\botdiplom\\chromedriver\\chromedriver-win64\\chromedriver.exe')


try:
    offset = 0
    url = f'https://magnit.ru/promo/?offset={offset}'

    driver.get(url=url)
    time.sleep(5)

    for cookie in pickle.load(open('cookie_spb', 'rb')):
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    lists = soup.find('ul', class_='paginate__container').find_all('li')[5].text

    with open('magnit.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
            )
        )

    for i in range(int(lists) - 1):
        driver.get(url=f'https://magnit.ru/promo/?offset={offset}')
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.find_all('a', class_='new-card-product')
        for card in cards:

            if card.find('div', class_='new-card-product__badge') and card.find('div', class_='new-card-product__price-regular'):
                product = card.find('div', class_="new-card-product__title").text


                prise_new = card.find('div', class_='new-card-product__price-regular').text

                prise_old = card.find('div', class_='new-card-product__price-old').text

                sale = card.find('div', class_='new-card-product__badge').text

                with open('magnit.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    writer.writerow(
                        (
                            product,
                            prise_old,
                            prise_new,
                            sale,
                        )
                    )
        offset += 36
        print(f'[X] страницы {i + 1} отсканирована')
    print('Файл успешно записан')




except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
import selenium
from selenium.webdriver.common.keys import Keys
import os
import time

chromedriver = "/Users/Angelina/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = selenium.webdriver.Chrome(chromedriver)
driver.get("https://edadeal.ru/")

search_field = driver.find_element_by_class_name('b-header__search-input')
search_field.send_keys('хамовники')

start_search = driver.find_element_by_class_name('b-header__search-button')
start_search.click()
time.sleep(1)


def sort_results():
    results = driver.find_element_by_id('view').find_elements_by_class_name('b-button__root')
    for result in results:
        try:
            sort_by = result.get_attribute('href')
        except selenium.common.exceptions.StaleElementReferenceException:
            pass
        if 'price' in sort_by:
            driver.get(sort_by)
    return 'sorted by price'


def get_discounts():
    sort_results()
    results = driver.find_element_by_id('view').find_elements_by_class_name('p-offers__offer')

    for result in results:
        description_element = result.find_element_by_class_name('b-offer__description')
        description = description_element.get_attribute('innerHTML').strip().replace('&nbsp;', ' ')

        shop_element = result.find_element_by_class_name('b-offer__retailer-icon')
        shop = shop_element.get_attribute('title').strip().replace('&nbsp;', ' ')

        new_price = result.find_element_by_class_name('b-offer__price-new').get_attribute('innerHTML').strip().replace('&nbsp;', ' ')

        try:
            old_price = result.find_element_by_class_name('b-offer__price-old').get_attribute('innerHTML').strip().replace('&nbsp;', ' ')
        except selenium.common.exceptions.NoSuchElementException:
            old_price = 'no old price'
        end_of_sale = result.find_element_by_class_name('b-offer__dates').get_attribute('innerHTML').strip().replace('&nbsp;', ' ')
        print(description, shop, new_price, old_price, end_of_sale)

try:
    pages = driver.find_element_by_id('view').find_element_by_class_name('b-pagination__root').find_elements_by_class_name('b-button__root')
    num_of_pages = len(pages) - 1
    for i in range(num_of_pages):
        get_discounts()
        pages = driver.find_element_by_id('view').find_element_by_class_name(
            'b-pagination__root').find_elements_by_class_name('b-button__root')
        next_page = pages[-1]
        driver.get(next_page.get_attribute('href'))
except:
    get_discounts()

driver.quit()



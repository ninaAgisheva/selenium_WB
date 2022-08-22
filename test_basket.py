import pytest
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


LINK = 'http://localhost/litecart/en/'


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    browser = webdriver.Chrome(options=chrome_options)
    #browser.implicitly_wait(10)

    yield browser

    browser.quit()


def test_basket(browser):
    browser.get(LINK)
    open_first_product(browser)
    add_product_to_basket(browser)
    counter_increase(browser, '1')
    go_back_to_the_main_page(browser)
    open_first_product(browser)
    add_product_to_basket(browser)
    counter_increase(browser, '2')
    go_back_to_the_main_page(browser)
    open_first_product(browser)
    add_product_to_basket(browser)
    counter_increase(browser, '3')
    go_back_to_the_main_page(browser)
    go_to_basket(browser)
    remove_produkt(browser)
    table_increase(browser, 2)
    remove_produkt(browser)
    table_increase(browser, 1)
    remove_produkt(browser)
    table_increase(browser, 0)


def open_first_product(browser):
    general_menu = browser.find_element_by_id('box-most-popular')
    products = general_menu.find_elements_by_class_name('link')
    duck = products[0]
    duck.click()


def add_product_to_basket(browser):
    if has_selector(browser):
        select_value(browser)
    add = browser.find_element_by_name('add_cart_product').click()

def has_selector(browser):
    try:
        browser.find_element_by_class_name('options')
        return True
    except NoSuchElementException:
        return False

def select_value(browser):
    browser.find_element_by_xpath("//select[@name='options[Size]']/option[@value='Small']").click()


def counter_increase(browser, param):
    wait = WebDriverWait(browser, 5)
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart > a.content > span.quantity') , param))


def get_crumbs(browser):
    crumbs = browser.find_elements_by_class_name('list-horizontal')[1]
    home = crumbs.find_elements_by_tag_name('li')[0]

    return home.find_element_by_tag_name('a')


def go_back_to_the_main_page(browser):
    get_crumbs(browser).click()


def get_link_cart(browser):
    cart = browser.find_element_by_id('cart')

    return cart.find_elements_by_tag_name('a')[2]


def go_to_basket(browser):
    get_link_cart(browser).click()


def remove_produkt(browser):
    browser.find_element_by_name('remove_cart_item').click()


def get_line_table(browser):
    table = browser.find_element_by_class_name('rounded-corners')

    return table.find_elements_by_tag_name('tr')


def table_increase(browser, param):
    table = get_line_table(browser)
    line_table = table[param]
    wait = WebDriverWait(browser, 5)
    wait.until(EC.staleness_of(line_table))





import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_working_with_cart(driver):
    # login
    driver.get("http://localhost/litecart/en/")

    # main test
    wait = WebDriverWait(driver, 10)
    locator_q = (By.CSS_SELECTOR, "#cart > a.content > span.quantity")
    quantity_number = int(driver.find_element(*locator_q).text)

    while quantity_number < 3:
        driver.find_element(By.CSS_SELECTOR, "#box-most-popular li:first-of-type > a.link").click()
        size_options = driver.find_elements(By.CSS_SELECTOR, "select[name='options[Size]']")
        if size_options:
            Select(size_options[0]).select_by_index(1)
        driver.find_element(By.CSS_SELECTOR, "button[name=add_cart_product]").click()
        wait.until(EC.text_to_be_present_in_element(locator_q, str(quantity_number + 1)))
        driver.get("http://localhost/litecart/en/")
        quantity_number = int(driver.find_element(*locator_q).text)

    driver.find_element(By.CSS_SELECTOR, "#cart > a.link").click()
    items = driver.find_elements(By.CSS_SELECTOR, "ul.items > li")
    while items:
        order_table = driver.find_element(By.CSS_SELECTOR, "table.dataTable")
        delete_buttons = driver.find_elements(By.CSS_SELECTOR, "button[name=remove_cart_item]")
        wait.until(EC.visibility_of(delete_buttons[0])).click()
        driver.refresh()
        wait.until(EC.staleness_of(order_table))
        items = driver.find_elements(By.CSS_SELECTOR, "ul.items > li")

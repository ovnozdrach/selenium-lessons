import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def test_browser_logs(driver):
    # login
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button_login = driver.find_element("name", "login")
    button_login.click()

    # main test
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    products = driver.find_elements(By.CSS_SELECTOR, "td:nth-child(3) > a[href*='_product']")
    links = [product.get_attribute('href') for product in products]
    for link in links:
        new_logs = []
        old_logs = driver.get_log("browser")
        driver.get(link)
        page = driver.find_element(By.CSS_SELECTOR, "h1").text
        logs = driver.get_log("browser")
        new_logs = list(set(logs) - set(old_logs))
        if new_logs:
            print(f"New logs for '{page}': \n{new_logs}")
        else:
            print(f"No new logs for '{page}' page")
        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_admin_items(driver):
    # login
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button_login = driver.find_element("name", "login")
    button_login.click()

    # main test
    main_items = driver.find_elements(By.CSS_SELECTOR, "#app-")
    for main_index, item in enumerate(main_items):
        driver.find_elements(By.CSS_SELECTOR, "#app-")[main_index].click()
        title = driver.find_element(By.CSS_SELECTOR, "#content > h1")
        assert title
        print(title.text)
        # sub_items test
        sub_items = driver.find_elements(By.CSS_SELECTOR, "#app- li")
        for index, _ in enumerate(sub_items):
            driver.find_elements(By.CSS_SELECTOR, "#app- li")[index].click()
            title = driver.find_element(By.CSS_SELECTOR, "#content > h1")
            assert title
            print(f"    {title.text}")

import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def test_login_admin(driver):
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button = driver.find_element("name", "login")
    button.click()

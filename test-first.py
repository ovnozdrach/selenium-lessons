import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("https://www.google.com")
    time.sleep(2)
    search_box = driver.find_element("name", "q")
    search_box.send_keys('webdriver')
    time.sleep(1)
    button = driver.find_element("name", "btnK")
    button.click()
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))

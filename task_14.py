import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # wd = webdriver.Firefox()
    wd.maximize_window()

    wd.implicitly_wait(5)
    request.addfinalizer(wd.quit)
    return wd


class there_is_window_other_than:
    def __init__(self, old_windows):
        self._old_windows = old_windows

    def __call__(self, driver):
        new_windows = list(set(driver.window_handles) - set(self._old_windows))
        return new_windows[0] if new_windows else False


def test_multiple_windows(driver):
    # login
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button_login = driver.find_element("name", "login")
    button_login.click()
    time.sleep(1)

    # main test
    wait = WebDriverWait(driver, 10)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element(By.CSS_SELECTOR, "#content > div > a.button").click()
    links = driver.find_elements(By.CSS_SELECTOR, "td > a[href^=http][target=_blank]")
    # new windows
    for link in links:
        main_window = driver.current_window_handle
        old_windows = driver.window_handles
        link.click()
        new_window = wait.until(there_is_window_other_than(old_windows))
        driver.switch_to.window(new_window)
        try:
            wait.until(lambda x: driver.execute_script('return document.readyState') == 'complete')
        except TimeoutException:
            print("\nTimeoutException")
        driver.close()
        driver.switch_to.window(main_window)

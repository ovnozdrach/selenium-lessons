import pytest
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

@pytest.fixture
def driver(request):
    # wd = webdriver.Chrome()
    wd = EventFiringWebDriver(webdriver.Chrome(), MyListener())
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(f"Locator: {by}, {value}")

    def after_find(self, by, value, driver):
        print(f"Locator: {by}, {value} found")

    def on_exception(self, exception, driver):
        print(f"Got an exception: {exception}")
        driver.get_screenshot_as_file('exception.png')
        print(f"Screenshot with exception: 'exception.png'")



def test_login_admin(driver):
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button = driver.find_element("name", "login")
    button.click()
    driver.get_screenshot_as_file('screen.png')

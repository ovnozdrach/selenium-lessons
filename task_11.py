import random
import string
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def driver(request):
    # wd = webdriver.Chrome()
    wd = webdriver.Firefox()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_user_registration(driver):
    # main page
    driver.get("http://localhost/litecart/en/")
    driver.find_element(By.CSS_SELECTOR, "form[name=login_form] > table > tbody > tr:nth-child(5) > td > a").click()

    # register
    driver.find_element(By.CSS_SELECTOR, "input[name=firstname]").send_keys("Some_name")
    driver.find_element(By.CSS_SELECTOR, "input[name=lastname]").send_keys("Some_surname")
    driver.find_element(By.CSS_SELECTOR, "input[name=address1]").send_keys("Some_address")
    index = random.randint(10001, 99999)
    driver.find_element(By.CSS_SELECTOR, "input[name=postcode]").send_keys(str(index))
    driver.find_element(By.CSS_SELECTOR, "input[name=city]").send_keys("Some_city")
    country = driver.find_element(By.CSS_SELECTOR, ".select2")
    ActionChains(driver).move_to_element(country).click().send_keys("United States").send_keys(Keys.RETURN).perform()
    email = ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + '@yandex.com'
    driver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(email)
    phone = random.randint(10000000000, 19999999999)
    driver.find_element(By.CSS_SELECTOR, "input[name=phone]").send_keys(str(phone))
    driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "input[name=confirmed_password]").send_keys("123")
    print(f"\nIndex: {index}\nEmail: {email}\nphone: {phone}")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[name=create_account]").click()
    # logout
    driver.find_element(By.CSS_SELECTOR, "#box-account > div > ul > li:nth-child(4) > a").click()
    # login
    driver.find_element(By.CSS_SELECTOR, "input[name=email]").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[name=login]").click()
    # logout
    driver.find_element(By.CSS_SELECTOR, "#box-account > div > ul > li:nth-child(4) > a").click()

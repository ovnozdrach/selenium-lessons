import os
import random
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(5)
    request.addfinalizer(wd.quit)
    return wd


def test_new_addition(driver):
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
    driver.find_element(By.CSS_SELECTOR, "#box-apps-menu > li:nth-child(2)").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#content > div:nth-child(2) > a:nth-child(2)").click()
    driver.find_element(By.CSS_SELECTOR, "input[name=status]").click()
    code = str(random.randint(1, 99999))
    name = f"duck_{code}"
    driver.find_element(By.CSS_SELECTOR, "input[name^='name'").send_keys(name)
    driver.find_element(By.CSS_SELECTOR, "input[name=code]").send_keys(code)
    driver.find_element(By.CSS_SELECTOR, "input[name=quantity]").send_keys("10")
    path = os.path.join(os.getcwd(), 'duck.jpg')
    driver.find_element(By.CSS_SELECTOR, "input[name^='new_images'").send_keys(path)
    driver.find_element(By.CSS_SELECTOR, "#content > form > div > ul > li:nth-child(2) > a").click()
    time.sleep(2)
    manufacture = Select(driver.find_element(By.CSS_SELECTOR, "select[name=manufacturer_id]"))
    manufacture.select_by_index(1)
    driver.find_element(By.CSS_SELECTOR, "input[name=keywords]").send_keys("Some short desc")
    driver.find_element(By.CSS_SELECTOR, "div.trumbowyg-editor").send_keys("Some description about product")
    driver.find_element(By.CSS_SELECTOR, "#content > form > div > ul > li:nth-child(4) > a").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "input[name=purchase_price]").send_keys("1")
    driver.find_element(By.CSS_SELECTOR, "input[name^='gross_prices[USD]'").send_keys("2")
    driver.find_element(By.CSS_SELECTOR, "button[name=save]").click()
    driver.find_element(By.XPATH, f"//a[.='{name}']").click()
    time.sleep(1)
    saved_code = driver.find_element(By.CSS_SELECTOR, "input[name=code]").get_attribute("value")

    assert saved_code == code, f"Saved product code for {name} should be {code} but got {saved_code}"

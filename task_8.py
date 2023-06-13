import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_country_order(driver):
    # login
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button_login = driver.find_element("name", "login")
    button_login.click()
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")

    # main test
    rows = driver.find_elements(By.CSS_SELECTOR, "#content > form > table > tbody > tr.row")
    countries = []
    multi_zone_countries = []
    for row in rows:
        name = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").get_attribute("textContent")
        countries.append(name)
        if row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").get_attribute("textContent") != "0":
            multi_zone_countries.append(name)
        assert True

    # check country list order
    assert countries == sorted(countries), f"The country list is not sorted: {countries}"
    print(f"The country list: {countries}")
    print(f"The multi zone countries: {multi_zone_countries}")

    for country in multi_zone_countries:
        print(f"Checking zones for country: {country}...")
        driver.find_element(By.XPATH, f"//*[contains(text(), {country})]").click()
        zones = driver.find_element(By.CSS_SELECTOR, "#table-zones > tbody > tr").get_attribute("textContent")
        assert zones == sorted(zones), f"The zone list is not sorted: {zones}"




import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd


def test_zone_order(driver):
    # login
    driver.get("http://localhost/litecart/admin")
    username_field = driver.find_element("name", "username")
    username_field.send_keys('admin')
    psw_field = driver.find_element("name", "password")
    psw_field.send_keys('admin')
    button_login = driver.find_element("name", "login")
    button_login.click()

    # main test
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody > tr.row > td:nth-child(3)")
    countries = [row.get_attribute("textContent") for row in rows]
    # check country list order
    print(f"The country list: {countries}")

    for country in countries:
        print(f"Checking zones for country: {country}")
        driver.find_element(By.XPATH, f"//a[.='{country}']").click()
        zones = driver.find_elements(By.CSS_SELECTOR, "[name*=zone_code] > [selected]")
        zone_list = [zone.get_attribute("textContent") for zone in zones]
        # check zone list order
        assert zone_list == sorted(zone_list), f"The zone list is not sorted: {zone_list}"
        print(f"The {country} zone list is sorted: {zone_list}")
        driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")

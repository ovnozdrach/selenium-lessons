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
    # main page
    driver.get("http://localhost/litecart")

    # main test
    goods = driver.find_elements(By.CSS_SELECTOR, ".products > li")
    for item in goods:
        stickers = item.find_elements(By.CSS_SELECTOR, ".sticker")
        assert len(stickers) == 1

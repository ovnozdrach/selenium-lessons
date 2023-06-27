import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver(request):
    proxy_url = "127.0.0.1:8080"
    options = Options()
    options.add_argument(f'--proxy-server={proxy_url}')
    # options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    wd = webdriver.Chrome(options=options)
    # wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def test_working_with_proxy(driver):
    # login
    driver.get("https://hub.cloud.mts.ru/")
    print(f'Page content: {driver.find_element(By.TAG_NAME, "body").text}')

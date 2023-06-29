from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/")
        return self

    @property
    def most_popular_products(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "#box-most-popular li > a.link")

    def open_most_popular_product(self):
        self.most_popular_products[0].click()

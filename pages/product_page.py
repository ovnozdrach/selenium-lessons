from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @property
    def cart_item_number(self):
        return int(self.driver.find_element(By.CSS_SELECTOR, "#cart > a.content > span.quantity").text)

    def product_size_select(self, index):
        size_options = self.driver.find_elements(By.CSS_SELECTOR, "select[name='options[Size]']")
        if size_options:
            Select(size_options[0]).select_by_index(index)
        return self

    def add_product_to_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[name=add_cart_product]").click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart > a.content > span.quantity"),
                                             str(self.cart_item_number + 1)))
        return self

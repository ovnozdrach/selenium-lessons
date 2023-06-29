from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/checkout")
        return self

    @property
    def order_items(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "ul.items > li")

    def order_item_delete(self):
        order_table = self.driver.find_element(By.CSS_SELECTOR, "table.dataTable")
        delete_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[name=remove_cart_item]")
        self.wait.until(EC.visibility_of(delete_buttons[0])).click()
        self.wait.until(EC.staleness_of(order_table))

from selenium import webdriver
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Firefox()
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def open(self):
        self.main_page.open()
        return self

    def add_popular_items_to_cart(self, number):
        for _ in range(number):
            self.main_page.open_most_popular_product()
            self.product_page.product_size_select(1).add_product_to_cart()
            self.main_page.open()

    def clear_cart(self):
        self.cart_page.open()
        while self.cart_page.order_items:
            self.cart_page.order_item_delete()

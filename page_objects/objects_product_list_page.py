from selenium.webdriver.common.by import By

class ProductListObjects:

    def __init__(self, driver):
        self.driver = driver

    products = (By.CSS_SELECTOR, ".inventory_item")

    def get_products_list(self):
        return self.driver.find_elements(*ProductListObjects.products)


# test package / test_demo.py
import pytest
from selenium.webdriver.common.by import By

from PytestPytonFramework.page_objects.objects_login_page import LogInObjects
from PytestPytonFramework.page_objects.objects_product_list_page import ProductListObjects
from PytestPytonFramework.test_data.data_login_page import LoginData
from PytestPytonFramework.utilities.base_class import BaseClass

# on-page fixture here plays role of regular func
# do not duplicate code and for TC2 & TC3 which use "items_list" to be independent
# "items_list" list of items showing on product page
@pytest.fixture
def fixture_items_on_product_page(fixture_browser_setup):
    driver = fixture_browser_setup
    # fixture_browser_setup in conftest.py file

    prod_list_page_driver = ProductListObjects(driver)
    # to pass driver as an argument to class constructor on Object page

    items_list = prod_list_page_driver.get_products_list()
    # driver.find_elements(By.CSS_SELECTOR, ".inventory_item")

    number_items_displayed = len(items_list)
    return items_list, number_items_displayed
# "fixture_browser_setup" from conftest.py file is executed once for the entre class


class TestProductPage(BaseClass):
    # TestSuite1 inherits properties of BaseClass decorated with @pytest.mark.usefixtures("fixture_browser_setup")
    # now should not declare '@pytest.mark.usefixtures()' in front of each class in each file (test suite)
    # from Pytest.utilities.BaseClass import BaseClass

    # in my case class name must start from 'Test', to be discovered by pytest
    # all test function must contain 'self' as argument because in the class
    # driver var is class var so "self.driver"

    # TC 1. Assertion of correct page to be opened
    def test_check_url(self):
        print("Swag Labs")  # demo for GIT
        assert "Swag Labs" in self.driver.title

    # TC 2. Log-in with Username (standard_user), password (secret_sauce)
    # "get_login_data" login data fixture set as a parameter of this test function
    def test_logIn(self, get_login_data):
        log = self.get_logger()
        # create var log and assign to this var get_logger method from BaseClass (child TestProductPage class)

        log.info("Logging in with different username and passwords")
        # set info message
        # can use get_logger method to print actual message from web-page log.info(var_text)
        # here var_text - var containing actual text from web page, method should follow var initialisation

        log_page_driver = LogInObjects(self.driver)
        #  create an instance of the LogIn class and assigns it to the variable log_page_driver
        # to pass driver as an argument to constructor on Object page

        self.driver.get("https://www.saucedemo.com/")

        log_page_driver.get_loging_field().send_keys(get_login_data["login"])
        # self.driver.find_element(By.CSS_SELECTOR, "#user-name").send_keys("standard_user")
        # call local object = class which contains loging_field() method on object page (Login_page.py)
        # get_login_data["login"] - login is a key in fixture dictionary

        log_page_driver.get_password_field().send_keys(get_login_data["password"])
        # self.driver.find_element(By.CSS_SELECTOR, ".input_error[type='password']").send_keys("secret_sauce")
        # get_login_data["password"] - password is a key in fixture dictionary

        log_page_driver.get_login_button().click()
        # self.driver.find_element(By.CSS_SELECTOR, "#login-button").click()

        # refresh after each set of tuple, otherwise will add (concatenate) value [0] + value[1] + value[3] in line
        # otherwise add  self.driver.get("https://www.saucedemo.com/") from conftest.py into this TC
        # self.driver.refresh()

    # TC 3. Verify min 'x' items displayed on page
    def test_min_number_of_items(self, fixture_items_on_product_page):
        log = self.get_logger()
        x = 6
        # unpack tuple passed from items_on_product_page fixture and get the second value (number_items_displayed)
        _, number_items_displayed = fixture_items_on_product_page
        log.info(f"Page displayed: {number_items_displayed} items")
        assert number_items_displayed >= x

    # TC 4. Add to cart first, last, and random item and go to cart
    def test_add_to_cart(self, fixture_items_on_product_page):
        import random
        # unpack tuple passed from items_on_product_page fixture and get both values
        items_list, _ = fixture_items_on_product_page
        _, number_items_displayed = fixture_items_on_product_page
        purchase_index_list = [0, number_items_displayed - 1, random.randrange(1, number_items_displayed - 1)]

        for index in purchase_index_list:
            items_list[index].find_element(By.CSS_SELECTOR, "div button").click()
            # chaining for buttons.
            # Call (list, not driver) by extension only since " div button" is  nested in ".inventory_item"
            # full CSS locator for buttons is ".inventory_item div button"

    # create fixture with different sets of login data from Exel
    # each set in dictionary {"key":"value"}
    # call this dictionary by calling method from data_login_page, class: LoginData, method: et_one_set_data()
    # test_case_name we would like to execute - parameter "Test_case_2"
    @pytest.fixture(params=LoginData.get_one_set_data("Test_case_2"))
    def get_login_data(self, request):
        return request.param
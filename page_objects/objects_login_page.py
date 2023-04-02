# create class with elements on LogIn page
from selenium.webdriver.common.by import By


class LogInObjects:

    # create constructor for this class and accept 'driver" as parameter from page with TC
    def __init__(self, driver):
        # set received driver argument as local driver
        self.driver = driver

    # create page object as a tuple (unchangeable)
    username = (By.CSS_SELECTOR, "#user-name")
    password = (By.CSS_SELECTOR, ".input_error[type='password']")
    log_button = (By.CSS_SELECTOR, "#login-button")

    # call  username object in method
    def get_loging_field(self):
        return self.driver.find_element(*LogInObjects.username)
        # driver.find_element(*ClassName.var_name) = driver.find_element(By.CSS_SELECTOR, "#user-name")
        # '*' - makes tuple to be unpacked into two separate arguments

    def get_password_field(self):
        return self.driver.find_element(*LogInObjects.password)


    def get_login_button(self):
        return self.driver.find_element(*LogInObjects.log_button)

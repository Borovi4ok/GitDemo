# file BaseClass.py
import inspect
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.support.wait import WebDriverWait
import logging


# define BaseClass to remove Fixture redundant code from child classes in all test files
@pytest.mark.usefixtures("fixture_browser_setup")
class BaseClass:

    # reusable func implicit wait (for certain condition: presence_of_element_located)
    # call func from any TC and send text as argument that should be present
    # e.g. self.verify_link_presence("some text")
    def verify_link_presence(self, text):
        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, text)))

    # create logger method to log results of TC
    def get_logger(self):
        logger_name = inspect.stack()[1][3]
        # way to dynamically determine the name of the calling TC in order to log messages with that TC name
        # otherwise will include in log BaseClass name only all the time

        logger = logging.getLogger(logger_name)
        # to ensure that the name of the current module (file with TC) is included in the final log message
        # creating object and as a argument of “getLogger” method pass “logger_name”

        file_handler = logging.FileHandler("logfile_test_demo.log")
        # giving name to the file that will contain log
        # here using FileHandler but can use different built-in handler classes (StreamHandler, SysLogHandler)
        # or can create custom handlers, but here we want to write log in a file not printing or send to console or over the network

        formatter = logging.Formatter("%(asctime)s :%(levelname)s :%(name)s :%(message)s")
        # # create object with specified format of the log message
        # “%(asctime)s - creates time stamp
        # : - separator
        # %(levelname)s - level name like warning, info, error etc.
        # %(name)s - name of the file
        # %(message)s - actual message that we create below for each log level

        file_handler.setFormatter(formatter)
        # attach formatter object to file_handler
        # send formatter object as an argument tofile Handler

        logger.addHandler(file_handler)
        # attach file_handler (which already knows format of message & file name) to logger
        # add the “File_handler” object to the “logger” object

        logger.setLevel(logging.INFO)
        # set level from which logger will include level messages in log file (start point)
        # means we will not see debug messages in log but INFO and all other with higher severity

        return logger

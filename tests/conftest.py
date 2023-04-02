# file conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# initializing driver var globally
driver = None


# "browser_name" - command line option
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="my option: what browser to use to run tests"
    )


# --browser_name is a key - command
# value for this command should be chrome or firefox ect.


# fixture file execute for TC, here entire class since (scope="class")
@pytest.fixture(scope="class")
def fixture_browser_setup(request):
    global driver
    # for driver to be accessible for _capture_screenshot()

    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        service_chrome = Service(r"C:\Disk D\Draft\QA Tester\Web Drivers\Chrome_webdriver.exe")
        # 'r' in front of path - raw string, to use a single backslashes
        driver = webdriver.Chrome(service=service_chrome)
    elif browser_name == "firefox":
        service_firefox = Service(r"C:\Disk D\Draft\QA Tester\Web Drivers\Firefox_gecko.exe")
        driver = webdriver.Chrome(service=service_firefox)
        # driver = webdriver.Firefox(executable_path=r"C:\Disk D\Draft\QA Tester\Web Drivers\Firefox_gecko.exe")
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    # declared driver will be sent to the class
    request.cls.driver = driver
    yield driver
    driver.quit()

# code - first func - that captures screenshot when TC failed and place in report
# @pytest.mark.hookwrapper - old-style way
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plagin to take and embed screenshot in html report, whenever test fails
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == "call" or report.when == "setup":
    # always add url to report
        extra.append(pytest_html.extras.url('http://www.example.com/'))
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screaenshot" style="width:304px;height;228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
                report.extra = extra
# code - second func - that captures screenshot when TC failed and place in report
def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)

'''
This module provides a function for executing a click on a WebElement 
using JavaScript instead of the standard WebDriver click method.
'''
# External
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper._types import MyWebDriver


def click_via_javascript(driver: MyWebDriver, job_button: WebElement):
    '''
    Executes a click on a WebElement using JavaScript instead of using the 
    standard WebDriver click method.

    - driver (MyWebDriver): A webdriver instance to use for executing the script.

    - job_button (WebElement): The WebElement to click on.
    '''

    # https://stackoverflow.com/a/48667924/12490791
    driver.execute_script("arguments[0].click();", job_button)

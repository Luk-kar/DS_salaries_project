'''
The module returns a webdriver for a specified URL, 
and if an error occurs, it returns a HTTP status code instead.
'''
# Python
import random
import sys
import time

# External
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException


# Internal
from scraper._types import MyWebDriver, WebElements
from scraper.config.get import get_config
from scraper.config._types import DebugMode
from scraper.jobs_to_csv.elements_query.await_element import await_element
from ._driver_getter import get_driver

config = get_config()


def get_webpage(
    url: str,
    country: str,
    debug_mode: DebugMode,
    driver_path: str = config['driver_path']
) -> MyWebDriver:
    '''returns browser driver'''

    driver: MyWebDriver = get_driver(debug_mode, driver_path)

    _get_url(url, driver)

    if country:

        search_bar = await_element(
            driver, 10, By.ID, "scBar"
        )
        country_input: WebElement = search_bar.find_element(
            By.ID, "sc.location"
        )
        country_input.send_keys(country)
        country_input.send_keys(Keys.ENTER)

        _wait_until_results_are_loaded(driver)

    return driver


def _get_url(url: str, driver: MyWebDriver):
    """
    Opens the specified URL in the browser driver provided, retrying up to 5-6 times if WebDriverException occurs.

    Args:
    - url: A string representing the URL to be opened.
    - driver: A Selenium WebDriver instance to control the browser window.

    Returns: None

    Raises: 
    - sys.exit: If WebDriverException occurs and the function is unable to open the URL after 5-6 retries.

    Usage: Call this function to open a URL in a browser window.
    """

    is_url = False
    chances = random.randint(5, 6)
    num_of_retries = chances
    while not is_url:
        try:
            driver.get(url)
            is_url = True
        except WebDriverException as error:
            if chances:
                chances -= 1
                time_span = random.uniform(4.0, 5.0)
                time.sleep(time_span)
            else:
                sys.exit(
                    f"\rCannot connect to the website after {num_of_retries} retries:\n{error}"
                )


def _wait_until_results_are_loaded(driver):
    """
    Waits for the job list buttons to be loaded on the webpage or load "no results".

    Args:
    - driver: A Selenium WebDriver instance to control the browser window.

    Returns: None

    Raises:
    - NoSuchElementException: If no job list buttons are found on the webpage.

    Usage: Call this function to wait until the job list buttons are loaded on the webpage.
    """

    jobs_list_buttons = await_element(
        driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

    try:
        jobs_buttons: WebElements = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li"
        )
    except NoSuchElementException as error:
        driver.quit()
        sys.exit(
            f"Check if you did not have any misspell in the job title or \
                    if you were silently blocked by glassdoor.\
                    \nError: {error}")

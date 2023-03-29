'''
The module returns a webdriver for a specified URL, 
and if an error occurs, it returns a HTTP status code instead.
'''
# Python
import time

# External
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper._types import MyWebDriver
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

    driver.get(url)

    # search country

    if country:

        search_bar = await_element(
            driver, 10, By.ID, "scBar"
        )
        # select country test field
        country_input: WebElement = search_bar.find_element(
            By.ID, "sc.location"
        )

        # submit_search = search_bar.find_element(
        #     By.XPATH, './/button[@type="submit"]'
        # )

        # Write the value
        country_input.send_keys(country)

        # Hit the enter
        country_input.send_keys(Keys.ENTER)

        time.sleep(100)

    return driver

'''
The module returns a webdriver for a specified URL, 
and if an error occurs, it returns a HTTP status code instead.
'''
# Python
import sys

# External
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    driver.get(url)

    if country:

        search_bar = await_element(
            driver, 10, By.ID, "scBar"
        )
        country_input: WebElement = search_bar.find_element(
            By.ID, "sc.location"
        )
        country_input.send_keys(country)
        country_input.send_keys(Keys.ENTER)

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

    return driver

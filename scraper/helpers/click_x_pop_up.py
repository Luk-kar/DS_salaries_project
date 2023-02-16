
# External
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)
from selenium.webdriver.common.by import By

# Internal
from scraper.helpers.await_element import await_element


def click_x_pop_up(driver):
    """riding off pop-up blocking web page elements"""

    try:
        x_button = await_element(
            driver, 3, By.CSS_SELECTOR, '[alt="Close"]')
        x_button.click()

    except (NoSuchElementException, TimeoutException):
        pass

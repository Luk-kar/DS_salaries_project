
# Python
from typing import Annotated, Type

# External
from annotated_types import Gt
from selenium.webdriver.support.wait import WebDriverWait

# Internal
from scraper._types import Element_XPATH, WebDriver


def await_element(driver: WebDriver, timeout: Annotated[int, Gt(0)], by: str, element: Element_XPATH) -> WebDriver:
    '''Use when the element loads in a run time after the initial load of the webpage'''

    return WebDriverWait(driver, timeout).until(
        lambda x: x.find_element(by, element))

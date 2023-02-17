
'''
This module contains a function that waits for an element
to load on a webpage at runtime and then returns the element
using the specified driver, timeout, XPATH element, and web element identifier.
'''
# Python
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Annotated


# External
from annotated_types import Gt
from selenium.webdriver.support.wait import WebDriverWait

# Internal
from scraper._types import Element_XPATH, WebElem


def await_element(
    driver: WebDriver | WebElem,
    timeout: Annotated[int, Gt(0)],
    by: str, element:
    Element_XPATH
) -> WebElem:
    '''Use when the element loads in a run time after the initial loading of the webpage'''

    return WebDriverWait(driver, timeout).until(
        lambda x: x.find_element(by, element))

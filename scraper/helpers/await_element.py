
# Python
from typing import Annotated, Type

# External
from annotated_types import Gt
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

# Internal
from scraper._types import Element_XPATH, Driver


def await_element(driver: Driver, timeout: Annotated[int, Gt(0)], by: Type[By], element: Element_XPATH) -> Driver:
    '''Use when the element loads in a run time after the initial load of the webpage'''

    return WebDriverWait(driver, timeout).until(
        lambda x: x.find_element(by, element))

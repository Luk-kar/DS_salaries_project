
# Python
from typing import Annotated

# External
from annotated_types import Gt
from selenium.webdriver.support.wait import WebDriverWait

# Internal
from _types import DriverChrome


def await_element(driver: DriverChrome, timeout: Annotated[int, Gt(0)], by, elem) -> DriverChrome:
    '''Use when the element loads in a run time after the initial load of the webpage'''

    return WebDriverWait(driver, timeout).until(
        lambda x: x.find_element(by, elem))

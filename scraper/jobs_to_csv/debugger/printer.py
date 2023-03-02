'''
This module provides a function
that prints key-value pairs for a Job object,
which is used for debugging when parsing HTML.
'''
# Python
import math
from os import get_terminal_size

# External
from selenium.webdriver.common.by import By

# Internal
from scraper._types import Job, MyWebDriver


def print_key_value_pairs(job: Job):
    '''used for debugging, when parsing HTML'''

    for index, (key, value) in enumerate(job.items()):
        print(f"{index + 1}. {key}:\n{value}")

    _print_separator("=")


def _print_separator(char_separator: str):
    '''
    Prints a separator line composed of a single character.

    Args:
    - char_separator: a string with a single character that will be repeated
    to compose the separator line.

    Returns: None
    '''

    terminal_width = get_terminal_size().columns
    separator = f"\n{char_separator * terminal_width}\n"
    print(separator)


def print_current_page(driver: MyWebDriver):
    '''
    Prints the current page number using web's the pagination footer text.

    Args:
    - driver: an instance of MyWebDriver class representing a web browser.

    Returns: None
    '''

    pagination_footer = _get_pagination_footer(driver)

    separator = "-"

    _print_separator(separator)

    print(pagination_footer)

    _print_separator(separator)


def _get_pagination_footer(driver: MyWebDriver):
    '''
    Get the pagination footer text from a job search result page using the driver object.

    Args:
    - driver: an instance of MyWebDriver class representing a web browser.

    Returns:
    - str: the pagination footer text
    '''

    return driver.find_element(
        By.XPATH, './/div[@data-test="pagination-footer-text"]'
    ).text

'''
This module provides type aliases for web scraping with Selenium.
'''

# External
from typing import TypedDict
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config._types import NA_value

Field_value = str | NA_value | bool | list[str]
WebElem = WebElement
Element_XPATH = str
Job_values = dict[str, Field_value]
Job_element = TypedDict(
    'Job_element', {
        'value': Field_value,
        'element': str,
        'is_list': bool}
)
Job_elements = dict[str, Job_element]
Job = dict[str, Job_values] | dict
Jobs = list[Job]

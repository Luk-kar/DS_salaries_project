# External
from selenium import webdriver

# Internal
from scraper.config._types import NA_value
from typing import Type

Field_value = str | NA_value
WebDriver = Type[webdriver.chrome.webdriver.WebDriver]
Element_XPATH = str
Job_values = dict[str, Field_value]
Job_element = dict['value': Field_value, 'element': str]
Job_elements = dict[str, Job_element]
Job = list[Job_values | None]

'''
This module provides type aliases for web scraping with Selenium.
'''

# External
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config._types import NA_value
from scraper.jobs_getter.elements_query.XPATH_text_getter import XpathListSearch, XpathSearch

MyWebDriver = WebDriver
MyWebElement = WebElement
MyWebElements = list[MyWebElement]
Field_value = str | int | float | NA_value | bool | list[str]
Element_XPATH = str
Job_values = dict[str, Field_value]
Job_elements = dict[str, XpathListSearch | XpathSearch]
Job = dict[str, Job_values] | dict
Jobs = list[Job]

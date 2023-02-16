# External
from selenium import webdriver

# Internal
from scraper.config._types import NA_value

DataFrame_value = str | NA_value
DriverChrome = webdriver.chrome.webdriver.WebDriver
Job_value = dict[str, DataFrame_value]
Job_value_element = dict['value': DataFrame_value, 'element': str]
Job_values = dict[str, Job_value_element]
Job = list[Job_value | None]

'''
This module provides a function to get a website driver 
with custom options for web scraping using selenium, 
webdriver_manager, with the option to enable/disable debug mode 
and specify the path to the Chrome driver.
'''
# Python
import sys

# External
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from scraper.config.get import get_config

config = get_config()


def get_driver(
        debug_mode: bool = config['debug_mode'],
        path: str = config['driver_path']):
    '''Returns website's driver with custom options'''

    options = webdriver.ChromeOptions()

    # to simulate human behavior for bot detection
    options.add_argument("USER AGENT")

    if not debug_mode:
        options.add_argument('headless')

    if path == "auto-install":
        service_obj = Service(ChromeDriverManager().install())
    else:
        try:
            service_obj = Service(path)
        except WebDriverException as error:
            sys.exit(
                f'Make sure your path or driver version is correct:\n{error}'
            )

    driver = webdriver.Chrome(  # type: ignore [call-arg]
        service=service_obj, options=options)
    return driver

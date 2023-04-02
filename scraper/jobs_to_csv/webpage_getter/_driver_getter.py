'''
This module provides a function to get a website driver 
with custom options for web scraping using selenium, 
webdriver_manager, with the option to enable/disable debug mode 
and specify the path to the Chrome driver.
'''
# Python
import sys
import re
import os

# External
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from scraper.config.get import get_config

config = get_config()


class InvalidDriverPathError(Exception):
    pass


class MyService(Service):
    ''''''

    def __init__(self, executable_path, port=0, service_args=None, log_path=None):
        if not os.path.exists(executable_path):
            raise InvalidDriverPathError(f'Invalid path: {executable_path}')

        # https://regex101.com/r/kYDr70/1
        if not re.search(r'^.*chrome(?:driver|)\.(exe|sh)?$|^.*chrome(?:driver|)$', executable_path, re.IGNORECASE):
            raise InvalidDriverPathError(f'Invalid file: {executable_path}')

        super().__init__(executable_path, port=port,
                         service_args=service_args, log_path=log_path)


def get_driver(
        debug_mode: bool = config['debug_mode'],
        path: str = config['driver_path']):
    '''Returns driver with custom options'''

    options = webdriver.ChromeOptions()

    _make_driver_stealthy(options)

    # todo debug_mode=True add headless mode

    if path == "auto-install":
        print("\rInstalling driver automatically...")
        service_obj = MyService(ChromeDriverManager().install())
    else:
        if debug_mode:
            print(f"\nUsing the driver:\n{path}")
        try:
            service_obj = MyService(path)

        except WebDriverException as error:
            sys.exit(
                f'Make sure your path or driver version is correct:\n{error}'
            )

    driver = webdriver.Chrome(  # type: ignore [call-arg]
        service=service_obj, options=options)
    return driver


def _make_driver_stealthy(options: webdriver.ChromeOptions):
    '''Adding arguments to a driver to avoid bot detection'''

    options.add_argument("USER AGENT")

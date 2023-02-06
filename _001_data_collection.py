"""
The module responsible for creating RAW data format,
from queries from defined:
    - job title
    - number of offers
Additional parameters are: 
    - driver's path for selected web browser
    - debug mode for development and debugging
Arguments could be passed from the global config data file or directly into the function.
"""
# Python
from typing import Any, Union
import time

# External
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, ElementClickInterceptedException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests
# import pandas as pd

# Internal
from config.get import get_config, get_url
from _types import DriverChrome

config = get_config()
JobsList = list[Union[dict[str, Any], None]]


def get_df_job_postings(
        job_title: str = config["jobs_titles"]["default"],
        jobs_number: int = config["jobs_number"],
        driver_path: str = config["driver_path"],
        debug_mode: bool = config["debug_mode"]
):
    """returns DataFrame object from searched phrase on glassdoor.com"""

    url = get_url(config)
    driver = get_webpage(url, debug_mode)
    jobs: JobsList = []

    while len(jobs) < jobs_number:

        rid_off_pop_ups(driver)

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(By.CSS_SELECTOR, "jl")


def rid_off_pop_ups(driver):
    """pass blocking pop-ups"""

    rid_off_sign_up(driver)

    # to simulate human behavior for bot detection
    time.sleep(.1)

    click_x_pop_up(driver)


def click_x_pop_up(driver):
    """pass pop-up"""

    try:
        driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click()
        print('x out worked')
    except NoSuchElementException:
        print('x out failed')


def rid_off_sign_up(driver):
    """pass pop-up"""

    try:
        driver.find_element(By.CLASS_NAME, "selected").click()
    except ElementClickInterceptedException:
        pass


def get_webpage(url, debug_mode):
    """returns browser driver"""

    driver: DriverChrome = get_driver(debug_mode)
    try:
        driver.get(url)
    except WebDriverException as error:
        status_code = requests.get(url, timeout=3).status_code
        print(
            f"Failed to upload the url: {error}\n Status code: {status_code}")

    return driver


def get_driver(
        debug_mode: bool = config["debug_mode"],
        path: str = config["driver_path"]) -> DriverChrome:
    """returns website driver with custom options"""

    options = webdriver.ChromeOptions()

    # to simulate human behavior for bot detection
    options.add_argument("USER AGENT")

    if debug_mode:
        options.add_argument('headless')

    # Change the path to where chromedriver/other browser is if you need to.
    driver = webdriver.Chrome(
        executable_path=path, options=options)
    driver.set_window_rect(width=1120, height=1000)
    return driver


if __name__ == "__main__":

    get_df_job_postings(debug_mode=True)  # test todo

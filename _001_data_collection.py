from config.get import get_config, get_url
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import requests
import time
from typing import Union
# import pandas as pd

config = get_config()
url = get_url(config)


def get_jobs(
        job_title=config["jobs_titles"]["default"],
        url=url,
        jobs_number=config["jobs_number"],
        driver_path=config["driver_path"],
        debug_mode: bool = config["debug_mode"]
):

    driver = get_webpage(url, debug_mode)
    jobs: list[dict[str, Union[str, int, bool]]] = []

    while len(jobs) < jobs_number:

        rid_off_pop_ups(driver)

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(By.CSS_SELECTOR, "jl")


def rid_off_pop_ups(driver):
    rid_off_sign_up(driver)

    time.sleep(.1)

    click_x_pop_up(driver)


def click_x_pop_up(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click()
        print(' x out worked')
    except NoSuchElementException:
        print(' x out failed')
        pass


def rid_off_sign_up(driver):
    try:
        driver.find_element(By.CLASS_NAME, "selected").click()
    except ElementClickInterceptedException:
        pass


def get_webpage(url, debug_mode):
    driver = get_driver(debug_mode)
    try:
        driver.get(url)
    except WebDriverException as error:
        status_code = requests.get(url, timeout=3).status_code
        print(
            f"Failed to upload the url: {error}\n Status code: {status_code}")

    return driver


def get_driver(
        debug_mode: bool = config["debug_mode"],
        path: str = config["driver_path"]) -> webdriver:  # type: ignore[valid-type]

    options = webdriver.ChromeOptions()
    options.add_argument("USER AGENT")

    if debug_mode:
        options.add_argument('headless')

    # Change the path to where chromedriver is if you need to.
    driver = webdriver.Chrome(
        executable_path=path, options=options)
    driver.set_window_rect(width=1120, height=1000)
    return driver


if __name__ == "__main__":

    get_jobs(debug_mode=True)

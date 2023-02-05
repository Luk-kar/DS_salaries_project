from config.get import get_config, get_url
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
# import time
# import pandas as pd

config = get_config()
url = get_url(config)


def get_jobs(
        job_title=config["jobs_titles"]["default"],
        url=url,
        driver_path=config["driver_path"],
        debug_mode: bool = config["debug_mode"]
):

    driver = get_driver(debug_mode)
    driver.get(url)


def get_driver(debug_mode: bool = config["debug_mode"], path: str = config["driver_path"]) -> webdriver:
    options = webdriver.ChromeOptions()

    if not debug_mode:
        options.add_argument('headless')

    # Change the path to where chromedriver is if you need to.
    driver = webdriver.Chrome(
        executable_path=path, options=options)
    driver.set_window_rect(width=1120, height=1000)
    return driver


get_jobs(debug_mode=True)

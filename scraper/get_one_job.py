from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

from config.get import get_config

config = get_config()


def get_one_job(url=config["url"]):

    # run chrome
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    options.set_window_size(1120, 1000)

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(
        executable_path=config["driver_path"], options=options)

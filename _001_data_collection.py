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
import random
from typing import Any, Union
import time

# External
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, ElementClickInterceptedException, WebDriverException, TimeoutException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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
    jobs_rows: JobsList = []

    while len(jobs_rows) < jobs_number:

        rid_off_pop_ups(driver)

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.

        jobs_list_buttons = await_element(
            driver, 10, By.XPATH, '//ul[@data-test="jlGrid"]')

        # jobs_list_buttons = driver.find_element(
        #     By.XPATH, '//ul[@data-test="jlGrid"]')

        jobs_buttons = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li")

        counter = 1
        for job_button in jobs_buttons:

            rand_sleep = random.uniform(0.5, 1.4)

            print("Progress: {}".format(
                "" + str(len(jobs_rows) + counter) + "/" + str(jobs_number)))
            if len(jobs_rows) >= jobs_number:
                break

            job_button.click()  # You might
            print("clicked", counter)

            counter += 1
            time.sleep(rand_sleep)
            collected_successfully = False

            job_column = await_element(
                driver, 5, By.ID, 'JDCol')

            click_x_pop_up(driver)

            company_name = job_column.find_element(
                By.XPATH, './/div[@data-test="employerName"]').text
            try:
                rating_overall = job_column.find_element(
                    By.XPATH, './/span[@data-test="detailRating"]').text
                company_name = company_name.replace(rating_overall, '')
            except NoSuchElementException:
                rating_overall = -1
            location = job_column.find_element(
                By.XPATH, './/div[@data-test="location"]').text
            job_title = job_column.find_element(
                By.XPATH, './/div[@data-test="jobTitle"]').text
            description = job_column.find_element(
                By.XPATH, './/div[@class="jobDescriptionContent desc"]').text

            try:
                salary_estimate = job_button.find_element(
                    By.XPATH, './/span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            if debug_mode:
                print(f"Job Title: {job_title}")
                print(f"Salary Estimate: {salary_estimate}")
                print(f"Job Description: {description[:500]}")
                print(f"Rating: {rating_overall}")
                print(f"Company Name: {company_name}")
                print(f"Location: {location}")


def await_element(driver, time, by, elem):
    return WebDriverWait(driver, time).until(
        lambda x: x.find_element(by, elem))


def rid_off_pop_ups(driver):
    """pass blocking pop-ups"""

    rid_off_sign_up(driver)

    # to simulate human behavior for bot detection
    time.sleep(.1)

    click_x_pop_up(driver)


def click_x_pop_up(driver):
    """pass pop-up"""

    try:
        x_button = await_element(
            driver, 3, By.CSS_SELECTOR, '[alt="Close"]')
        x_button.click()
        print('x out worked')
    except (NoSuchElementException, TimeoutException):
        print('x out failed')


def rid_off_sign_up(driver):
    """pass pop-up"""

    try:
        driver.find_element(By.CLASS_NAME, "selected").click()
    except (ElementClickInterceptedException, NoSuchElementException):
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

    if not debug_mode:
        options.add_argument('headless')

    # Change the path to where chromedriver/other browser is if you need to.
    driver = webdriver.Chrome(
        executable_path=path, options=options)
    # driver.set_window_rect(width=1120, height=1000)
    return driver


if __name__ == "__main__":

    get_df_job_postings(debug_mode=True)  # test todo

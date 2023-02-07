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

        jobs_list_buttons = await_element(
            driver, 10, By.XPATH, '//ul[@data-test="jlGrid"]')

        jobs_buttons = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li")

        NA_value = -1

        for job_button in jobs_buttons:

            print("Progress: {}".format(
                "" + str(len(jobs_rows) + 1) + "/" + str(jobs_number)))
            if len(jobs_rows) >= jobs_number:
                break

            job_button.click()

            rand_sleep = random.uniform(0.5, 1.4)
            time.sleep(rand_sleep)

            job_column = await_element(
                driver, 10, By.ID, 'JDCol')

            click_x_pop_up(driver)

            job_description = {
                "Company Name": {"value": NA_value, "element": './/div[@data-test="employerName"]'},
                "Rating": {"value": NA_value, "element": './/span[@data-test="detailRating"]'},
                "Location":  {"value": NA_value, "element": './/div[@data-test="location"]'},
                "Job Title":  {"value": NA_value, "element": './/div[@data-test="jobTitle"]'},
                "Description":  {"value": NA_value, "element": './/div[@class="jobDescriptionContent desc"]'},
                "Salary":  {"value": NA_value, "element": './/span[@data-test="detailSalary"]'},
            }

            get_info(job_column, job_description)

            try:
                job_description['Salary']['value'] = job_button.find_element(
                    By.XPATH, './/span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                job_description['Salary']['value'] = NA_value

            if debug_mode:
                for key, value in job_description.items():
                    v = value['value']
                    v = v[:500] if type(v) is str else v
                    print(f"{key}: {v}")

            company_column = {
                "Size": NA_value,
                "Type": NA_value,
                "Sector": NA_value,
                "Founded": NA_value,
                "Industry": NA_value,
                "Revenue": NA_value
            }

            try:
                company_info = job_column.find_element(By.ID, "EmpBasicInfo")

                for k in company_column.keys():
                    try:
                        company_column[k] = get_employer_info(company_info, k)
                    except NoSuchElementException:
                        pass

            except NoSuchElementException:
                pass

            if debug_mode:
                print_key_value_pairs(company_column)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


def get_info(job_column, job_description):

    for values in job_description.values():
        try:
            values['value'] = get_job_info(
                job_column, values['element'])
        except NoSuchElementException:
            pass
    return job_description


def get_job_info(job_column, values):
    return job_column.find_element(
        By.XPATH, values
    ).text


def print_key_value_pairs(values):
    for k, v in values.items():
        print(f"{k}: {v}")


def get_employer_info(employer_info, category):
    return employer_info.find_element(
        By.XPATH, f'.//div//*[text() = "{category}"]//following-sibling::*'
    ).text


def print_job_description(job_title, company_name, rating_overall, location, description, salary_estimate):
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

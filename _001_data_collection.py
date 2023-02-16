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
import sys
import time
from typing import Annotated
from annotated_types import Gt

# External
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
    NoSuchElementException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests

# Internal
from config.get import get_config, get_url
from config._types import NA_value
from _types import DriverChrome

config = get_config()
DataFrame_value = str | NA_value
Job_value = dict[str, DataFrame_value]
Job_value_element = dict['value': DataFrame_value, 'element': str]
Job_values = dict[str, Job_value_element]
Job = list[Job_value | None]


def get_df_job_postings(
        job_title: str = config["jobs_titles"]["default"],
        jobs_cap: Annotated[int, Gt(0)] = config["jobs_number"],
        driver_path: str = config["driver_path"],
        debug_mode: bool = config["debug_mode"]
):
    """returns uncleaned DataFrame object from searched phrase on glassdoor.com"""

    url = get_url(config['url'], job_title)
    driver = get_webpage(url, debug_mode, driver_path)
    jobs = []
    print("")  # \n

    while len(jobs) < jobs_cap:

        jobs_list_buttons = await_element(
            driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

        jobs_buttons = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li")

        click_x_pop_up(driver)

        for job_button in jobs_buttons:

            print(f"Progress: {len(jobs) + 1}/{jobs_cap}")

            if len(jobs) >= jobs_cap:
                break

            job_button.click()

            pause()

            click_x_pop_up(driver)

            job_row = get_job_row(debug_mode, driver, job_button)


def get_job_row(debug_mode, driver, job_button):

    job_row = {}

    na_value = config["NA_value"]

    job_post = await_element(
        driver, 10, By.ID, 'JDCol')

    pause()

    job_description: Job_values = {
        "Company_Name": {
            "value": na_value,
            "element": './/div[@data-test="employerName"]',
            "is_list": False
        },
        "Rating": {
            "value": na_value,
            "element": './/span[@data-test="detailRating"]',
            "is_list": False
        },
        "Location":  {
            "value": na_value,
            "element": './/div[@data-test="location"]',
            "is_list": False
        },
        "Job_Title":  {
            "value": na_value,
            "element": './/div[@data-test="jobTitle"]',
            "is_list": False
        },
        "Description":  {
            "value": na_value,
            "element": './/div[@class="jobDescriptionContent desc"]',
            "is_list": False
        },
        "Salary":  {
            "value": na_value,
            "element": './/span[@data-test="detailSalary"]',
            "is_list": False
        },
    }

    job_row = add_columns_to_row_from_source(
        job_row,
        job_post, job_description
    )

    job_button_info = {
        "Job_age": {
            "value": na_value,
            "element": './/div[@data-test="job-age"]',
            "is_list": False
        },
        "Easy_apply": {
            "value": na_value,
            "element": './/div[@class="css-pxdlb2"]/div[1]',
            "is_list": False
        },
    }

    job_row = add_columns_to_row_from_source(
        job_row,
        job_button, job_button_info
    )

    company_description: Job_values = {
        "Size": {
            'value': na_value,
            "element": './/div//*[text() = "Size"]//following-sibling::*',
            "is_list": False
        },
        "Type_of_ownership": {
            'value': na_value,
            "element": './/div//*[text() = "Type"]//following-sibling::*',
            "is_list": False
        },
        "Sector": {
            'value': na_value,
            "element": './/div//*[text() = "Sector"]//following-sibling::*',
            "is_list": False
        },
        "Founded": {
            'value': na_value,
            "element": './/div//*[text() = "Founded"]//following-sibling::*',
            "is_list": False
        },
        "Industry": {
            'value': na_value,
            "element": './/div//*[text() = "Industry"]//following-sibling::*',
            "is_list": False
        },
        "Revenue": {
            'value': na_value,
            "element": './/div//*[text() = "Revenue"]//following-sibling::*',
            "is_list": False
        },
    }

    try:
        company_info = job_post.find_element(By.ID, "EmpBasicInfo")

        job_row = add_columns_to_row_from_source(
            job_row,
            company_info, company_description
        )

    except NoSuchElementException:
        job_row = add_values_to_row_from_dict(
            job_row,
            company_description
        )

    rating_description: Job_values = {
        "Friend_recommend": {
            "value": na_value,
            "element": './/div[@class="css-ztsow4"]',
            "is_list": False
        },
        "CEO_approval": {
            "value": na_value,
            "element": './/div[@class="css-ztsow4 ceoApprove"]',
            "is_list": False
        },
        "Career_Opportunities": {
            "value": na_value,
            "element": './/*[text() = "Career Opportunities"]/following-sibling::span[2]',
            "is_list": False
        },
        "Comp_&_Benefits": {
            "value": na_value,
            "element": './/*[text() = "Comp & Benefits"]/following-sibling::span[2]',
            "is_list": False
        },
        "Culture_&_Values": {
            "value": na_value,
            "element": './/*[text() = "Culture & Values"]/following-sibling::span[2]',
            "is_list": False
        },
        "Senior_Management": {
            "value": na_value,
            "element": './/*[text() = "Senior Management"]/following-sibling::span[2]',
            "is_list": False
        },
        "Work/Life_Balance": {
            "value": na_value,
            "element": './/*[text() = "Work/Life_Balance"]/following-sibling::span[2]',
            "is_list": False
        },
    }

    try:
        rating_info: DriverChrome = job_post.find_element(
            By.XPATH, '//div[@data-test="company-ratings"]'
        )

        job_row = add_columns_to_row_from_source(
            job_row,
            rating_info, rating_description
        )

    except NoSuchElementException:
        job_row = add_values_to_row_from_dict(
            job_row,
            rating_description
        )

    reviews_by_job_title: Job_values = {
        "Pros": {
            "value": na_value,
            "element": './/*[text() = "Pros"]//parent::div//*[contains(name(), "p")]',
            "is_list": True
        },
        "Cons": {
            "value": na_value,
            "element": './/*[text() = "Cons"]//parent::div//*[contains(name(), "p")]',
            "is_list": True
        },
    }

    try:
        reviews_info: DriverChrome = job_post.find_element(
            By.ID, "Reviews"
        )
        job_row = add_columns_to_row_from_source(
            job_row,
            reviews_info, reviews_by_job_title
        )

    except NoSuchElementException:
        job_row = add_values_to_row_from_dict(
            job_row,
            reviews_by_job_title
        )

    benefits_review: Job_values = {
        "Benefits_rating": {
            "value": na_value,
            "element": '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div//div[@class="ratingNum mr-sm"]',
            "is_list": False
        },
        "Benefits_reviews": {
            "value": na_value,
            "element": '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div',
            "is_list": True
        },
    }

    try:
        job_row = add_columns_to_row_from_source(
            job_row,
            job_post, benefits_review
        )

    except NoSuchElementException:
        job_row = add_values_to_row_from_dict(job_row, benefits_review)

    if debug_mode:
        print_key_value_pairs(job_row)

    return job_row


def add_columns_to_row_from_source(job_row, values_source, values_to_add):

    values_to_add: Job_values = get_values(
        values_source, values_to_add)

    job_row = add_values_to_row_from_dict(job_row, values_to_add)

    return job_row


def print_key_value_pairs(job: Job):
    '''used for debugging, when parsing html'''

    for index, (key, value) in enumerate(job.items()):
        print(f"{index + 1}. {key}:\n{value}")

    print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")


def add_values_to_row_from_dict(job: Job, job_description: Job_values) -> Job:
    '''populate row for DataFrame object'''

    for key, value in job_description.items():
        job[key] = value["value"]

    return job


def pause():
    '''Pause for bot detection or to load things from page'''

    random_sleep = random.uniform(0.5, 1.4)
    time.sleep(random_sleep)


def get_values(source_html: DriverChrome, job_values):
    '''get values for each element in the list'''

    for values in job_values.values():
        try:
            values['value'] = get_XPATH_text(
                source_html, values['element'], values["is_list"])
        except NoSuchElementException:
            pass

    return job_values


def get_XPATH_text(source_html: DriverChrome, element: str, return_list=False):
    '''return text or texts of selected element'''

    if return_list:

        elements = source_html.find_elements(
            By.XPATH, element
        )

        texts: dict[str] = []
        for elem in elements:
            texts.append(elem.text)

        if not texts:
            texts = config["NA_value"]

        return texts

    text: str = source_html.find_element(
        By.XPATH, element
    ).text

    text = config["NA_value"] if text == "N/A" else text

    return text


def await_element(driver: DriverChrome, timeout: Annotated[int, Gt(0)], by, elem) -> DriverChrome:
    '''use when element do not load at initial webpage loading'''

    return WebDriverWait(driver, timeout).until(
        lambda x: x.find_element(by, elem))


def click_x_pop_up(driver):
    """rid off pop-up"""

    try:
        x_button = await_element(
            driver, 3, By.CSS_SELECTOR, '[alt="Close"]')
        x_button.click()

    except (NoSuchElementException, TimeoutException):
        pass


def get_webpage(url, debug_mode, driver_path: str = config["driver_path"]):
    """returns browser driver"""

    driver: DriverChrome = get_driver(debug_mode, driver_path)
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

    if path == "auto-install":
        service_obj = Service(ChromeDriverManager().install())
    else:
        try:
            service_obj = Service(path)
        except WebDriverException as error:
            sys.exit(
                f'Make sure your path or driver version is correct:\n{error}'
            )

            # auto-install if not existing
    driver = webdriver.Chrome(
        service=service_obj, options=options)
    # driver.set_window_rect(width=1120, height=1000)
    return driver


if __name__ == "__main__":

    get_df_job_postings(
        debug_mode=True, job_title="back end engineer")

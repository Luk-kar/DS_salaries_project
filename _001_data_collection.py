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

        na_value = config["NA_value"]

        view_table = await_element(
            driver, 5, By.XPATH, '//div[@data-test="JobDetailsFooter"]/div[2]//span')
        print(view_table.text)

        pause()

        view_table.click()  # todo
        # todo grab all links
        # todo add links at the end

        for job_button in jobs_buttons:

            print(f"Progress: {len(jobs) + 1}/{jobs_cap}")

            if len(jobs) >= jobs_cap:
                break

            job_button.click()

            pause()

            click_x_pop_up(driver)

            job_button.click()

            job_column = await_element(
                driver, 10, By.ID, 'JDCol')

            pause()

            job = {}

            job_description: Job_values = {
                "Company_Name": {
                    "value": na_value,
                    "element": './/div[@data-test="employerName"]'
                },
                "Rating": {
                    "value": na_value,
                    "element": './/span[@data-test="detailRating"]'
                },
                "Location":  {
                    "value": na_value,
                    "element": './/div[@data-test="location"]'
                },
                "Job_Title":  {
                    "value": na_value,
                    "element": './/div[@data-test="jobTitle"]'
                },
                "Description":  {
                    "value": na_value,
                    "element": './/div[@class="jobDescriptionContent desc"]'
                },
                "Salary":  {
                    "value": na_value,
                    "element": './/span[@data-test="detailSalary"]'
                },
            }

            job_description: Job_values = get_values(
                job_column, job_description)

            job = add_values_to_job(job, job_description)

            job_button_info = {
                "Job_age": {
                    "value": na_value, "element": './/div[@data-test="job-age"]'
                },
                "Easy_apply": {
                    "value": na_value, "element": './/div[@class="css-pxdlb2"]/div[1]'
                },
            }

            job_button_info = get_values(job_button, job_button_info)

            job = add_values_to_job(job, job_button_info)

            company_description: Job_values = {
                "Size": {
                    'value': na_value,
                    "element": './/div//*[text() = "Size"]//following-sibling::*'
                },
                "Type_of_ownership": {
                    'value': na_value,
                    "element": './/div//*[text() = "Type"]//following-sibling::*'
                },
                "Sector": {
                    'value': na_value,
                    "element": './/div//*[text() = "Sector"]//following-sibling::*'
                },
                "Founded": {
                    'value': na_value,
                    "element": './/div//*[text() = "Founded"]//following-sibling::*'
                },
                "Industry": {
                    'value': na_value,
                    "element": './/div//*[text() = "Industry"]//following-sibling::*'
                },
                "Revenue": {
                    'value': na_value,
                    "element": './/div//*[text() = "Revenue"]//following-sibling::*'
                },
            }

            try:
                company_info = job_column.find_element(By.ID, "EmpBasicInfo")
                company_description = get_values(
                    company_info, company_description)

            except NoSuchElementException:
                pass

            job = add_values_to_job(job, company_description)

            rating_description: Job_values = {
                "Friend_recommend": {
                    "value": na_value,
                    "element": './/div[@class="css-ztsow4"]'
                },
                "CEO_approval": {
                    "value": na_value,
                    "element": './/div[@class="css-ztsow4 ceoApprove"]'
                },
                "Career_Opportunities": {
                    "value": na_value,
                    "element": './/*[text() = "Career Opportunities"]/following-sibling::span[2]'
                },
                "Comp_&_Benefits": {
                    "value": na_value,
                    "element": './/*[text() = "Comp & Benefits"]/following-sibling::span[2]'
                },
                "Culture_&_Values": {
                    "value": na_value,
                    "element": './/*[text() = "Culture & Values"]/following-sibling::span[2]'
                },
                "Senior_Management": {
                    "value": na_value,
                    "element": './/*[text() = "Senior Management"]/following-sibling::span[2]'
                },
                "Work/Life_Balance": {
                    "value": na_value,
                    "element": './/*[text() = "Work/Life_Balance"]/following-sibling::span[2]'
                },
            }

            try:
                rating_info: DriverChrome = job_column.find_element(
                    By.XPATH, '//div[@data-test="company-ratings"]'
                )

                rating_description = get_values(
                    rating_info, rating_description
                )

            except NoSuchElementException:
                pass

            job = add_values_to_job(job, rating_description)

            reviews_by_job_title: Job_values = {
                "Pros": {
                    "value": na_value,
                    "element": './/*[text() = "Pros"]//parent::div//*[contains(name(), "p")]'
                },
                "Cons": {
                    "value": na_value,
                    "element": './/*[text() = "Cons"]//parent::div//*[contains(name(), "p")]'
                },
            }

            try:
                reviews_info: DriverChrome = job_column.find_element(
                    By.ID, "Reviews"
                )

                reviews_by_job_title = get_values(
                    reviews_info, reviews_by_job_title, return_list=True
                )
            except NoSuchElementException:
                pass

            job = add_values_to_job(job, reviews_by_job_title)

            benefits_rating: Job_values = {
                "Benefits_rating": {
                    "value": na_value,
                    "element": '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div//div[@class="ratingNum mr-sm"]'
                }
            }
            benefits_review: Job_values = {
                "Benefits_reviews": {
                    "value": na_value,
                    "element": '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div'
                },
            }

            try:
                benefits_rating = get_values(
                    job_column, benefits_rating)
                benefits_review = get_values(
                    job_column, benefits_review, return_list=True)
            except NoSuchElementException:
                pass

            job = add_values_to_job(job, benefits_rating)
            job = add_values_to_job(job, benefits_review)

            # todo add links at the end
            link: Job_values = {
                "Benefits_reviews": {
                    "value": na_value
                },
            }
            # job = add_values_to_job(job, link)

            if debug_mode:
                print_key_value_pairs(job)


def print_key_value_pairs(job: Job):
    '''used for debugging, when parsing html'''

    for index, (key, value) in enumerate(job.items()):
        print(f"{index + 1}. {key}:\n{value}")

    print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")


def add_values_to_job(job: Job, job_description: Job_values) -> Job:
    '''populate row for DataFrame object'''

    for key, value in job_description.items():
        job[key] = value["value"]

    return job


def pause():
    '''Pause for bot detection or to load things from page'''

    random_sleep = random.uniform(0.5, 1.4)
    time.sleep(random_sleep)


def get_values(source_html: DriverChrome, job_values, return_list=False):
    '''get values for each element in the list'''

    for values in job_values.values():
        try:
            values['value'] = get_XPATH_text(
                source_html, values['element'], return_list)
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

# Python
from datetime import datetime

# External
from selenium.webdriver.common.by import By

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper._types import WebDriver
from scraper.helpers.await_element import await_element
from scraper.helpers.click_x_pop_up import click_x_pop_up
from scraper.helpers.get_one_job import get_one_job
from scraper.helpers.pause import pause


def get_jobs(jobs_number: JobNumber, debug_mode: DebugMode, driver: WebDriver):
    '''Getting pandas dataframe populated with jobs from glassdoor.com'''

    jobs = []

    if debug_mode:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"\n{now}\n")

    while len(jobs) < jobs_number:
        jobs_list_buttons: WebDriver = await_element(
            driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

        jobs_buttons: list[WebDriver] = jobs_list_buttons.find_elements(
            By.TAG_NAME, "li")

        click_x_pop_up(driver)

        for job_button in jobs_buttons:
            print(f"Progress: {len(jobs) + 1}/{jobs_number}")

            if len(jobs) >= jobs_number:
                break

            job_button.click()

            pause()

            click_x_pop_up(driver)

            job = get_one_job(debug_mode, driver, job_button)

            jobs.append(job)

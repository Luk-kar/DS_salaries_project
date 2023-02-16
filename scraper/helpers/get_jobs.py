
# External
from selenium.webdriver.common.by import By

# Internal
from scraper.helpers.await_element import await_element
from scraper.helpers.click_x_pop_up import click_x_pop_up
from scraper.helpers.get_one_job import get_one_job
from scraper.helpers.pause import pause


def get_jobs(jobs_cap, debug_mode, driver):
    '''Getting pandas dataframe populated with jobs from glassdoor.com'''

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

            job = get_one_job(debug_mode, driver, job_button)

            jobs.append(job)

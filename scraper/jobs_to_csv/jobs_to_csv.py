# Python
import csv
from datetime import datetime
import os
import sys

# External
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config._types import JobNumber, DebugMode
from scraper.config.get import get_path_csv_raw
from scraper._types import MyWebDriver
from .elements_query.await_element import await_element
from .actions.click_javascript import click_via_javascript
from .actions.click_next_page import click_next_page
from .actions.click_x_pop_up import click_x_pop_up
from .job_value_getter.job_value_getter import get_values_for_job
from .actions.pause import pause
from .job_parser.job_parser import parse_data
from .debugger.print_key_value_pairs import print_key_value_pairs

WebElements = list[WebElement]


def get_jobs_to_csv(jobs_number: JobNumber, debug_mode: DebugMode, driver: MyWebDriver):
    '''Getting list of job postings values populated with glassdoor.com'''

    if debug_mode:
        now = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"\n{now}\n")

    jobs_counter = 1

    csv_writer = CSV_Writer_RAW()

    while jobs_counter <= jobs_number:

        jobs_list_buttons: WebElement = await_element(
            driver, 20, By.XPATH, '//ul[@data-test="jlGrid"]')

        try:
            jobs_buttons: WebElements = jobs_list_buttons.find_elements(
                By.TAG_NAME, "li"
            )
        except NoSuchElementException as error:
            sys.exit(
                f"Check if you did not any misspell in the job title or \
                if you were silently blocked by glassdoor.\
                \nError: {error}")

        click_x_pop_up(driver)

        for job_button in jobs_buttons:

            print(f"Progress: {jobs_counter}/{jobs_number}")

            if jobs_counter >= jobs_number + 1:
                break

            try:
                job_button.click()

            except ElementClickInterceptedException:

                click_via_javascript(driver, job_button)

            pause()

            click_x_pop_up(driver)

            job = get_values_for_job(driver, job_button)

            parse_data(job)

            if debug_mode:
                print_key_value_pairs(job)

            # write job to csv
            csv_writer.write_row(job)

            jobs_counter += 1

        click_next_page(driver, jobs_counter, jobs_number)


class CSV_Writer():

    def __init__(self, csv_path) -> None:
        self.csv_path = csv_path
        self.directory_path = os.path.dirname(csv_path)

    def write_row(self, row):
        '''
        appends list of tuples in specified output csv file
        a tuple is written as a single row in csv file
        '''
        file_path = self.csv_path

        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        if not os.path.isfile(self.csv_path):
            pass

        row = self.convert_dict_values_to_tuple(row)

        print(f"Row_to_save:\n{row}")

        with open(file_path, 'a', newline='', encoding="utf-8") as csv_file:

            csv_writer = csv.writer(csv_file)

            try:
                csv_writer.writerow(row)

            except csv.Error as error:
                sys.exit(
                    f'File:\n\
                    {file_path}\n\
                    Line:\
                    \n{csv_writer.line_num}\
                    \n Error:\
                    \n{error}'
                )

    def convert_dict_values_to_tuple(self, dictionary: dict) -> tuple:
        return tuple(dictionary.values())

    def write_header(self, header):  # todo
                with open(file_path, 'a', newline='', encoding="utf-8") as csv_file:

            csv_writer = csv.writer(csv_file)

            try:
                csv_writer.writerow(row)

            except csv.Error as error:
                sys.exit(
                    f'File:\n\
                    {file_path}\n\
                    Line:\
                    \n{csv_writer.line_num}\
                    \n Error:\
                    \n{error}'
                )



class CSV_Writer_RAW(CSV_Writer):

    def __init__(self) -> None:
        super().__init__(
            get_path_csv_raw()
        )

'''
This module contains a unit test for the scrape_data function in the scraper module. 
The TestIntegration class tests whether the CSV file created by 
the function follows a set of expected regex patterns. 
Two test methods are defined, one for running the function in debug mode and 
the other in production mode.
'''

# Python
import csv
import os
import random
import re
import unittest
from time import sleep
import _csv

# Internal
from scraper.config.get import get_encoding, get_path_csv_raw, get_config
from scraper.scraper import scrape_data


class TestIntegration(unittest.TestCase):
    '''
    Short test. If you want to test for longer periods run the scraper for several minutes.
    '''

    @classmethod
    def setUpClass(cls):
        '''init all config values'''

        regex = {
            # https://regex101.com/r/9m7gaB/1
            'Non-empty-string': r"^(?!\s*$).+",
            # https://regex101.com/r/XRho9L/1
            '0.0-5.0': r"^(?:[0-4](?:\.[0-9])?|5(?:\.0)?|)$",
            # https://regex101.com/r/vLx7JS/1
            '24h-30d+': r"^(?:24h|1 day ago|[1-2]?[0-9]d?|30d\+?)$",
            # https://regex101.com/r/9bIQDf/1
            'bool': r"^(True|False)$",
            # https://regex101.com/r/8TbXbC/1
            'employees': r"^(?!.*employees).*$",
            # https://regex101.com/r/g076Ht/1
            'exists': r"^.*$",
            # https://regex101.com/r/j32tP1/1
            '1-9999': r"^(?:[1-9]\d{0,3}|)$",
            # https://regex101.com/r/jVaJDa/1
            'Revenue_USD': r"^(?!.*\(USD\)).*$",
            # https://regex101.com/r/phTDbC/1
            '0.00-5.00': r"^(?:0(\.[0-9]{1,2})?|([1-4](\.[0-9]{1,2})?)|5(\.0{1,2})?|)$",
            # https://regex101.com/r/bGQCzp/1
            'reviews': r"^(\[((\'|\").*(\'|\")(, )?)+\]|)$"
        }

        cls.jobs_number = 3
        cls.csv = {
            'delimiter': ",",
            'encoding': get_encoding(),
            'expected_values': {
                'Company_name': regex["Non-empty-string"],
                'Rating': regex['0.0-5.0'],
                'Location': regex['Non-empty-string'],
                'Job_title': regex['Non-empty-string'],
                'Description': regex['Non-empty-string'],
                'Job_age': regex['24h-30d+'],
                'Easy_apply': regex['bool'],
                'Employees': regex['employees'],
                'Type_of_ownership': regex['exists'],
                'Sector': regex['exists'],
                'Founded': regex['1-9999'],
                'Industry': regex['exists'],
                'Revenue_USD': regex['Revenue_USD'],
                'Friend_recommend': regex['0.00-5.00'],
                'CEO_approval': regex['0.00-5.00'],
                'Career_opportunities': regex['0.0-5.0'],
                'Comp_&_benefits': regex['0.0-5.0'],
                'Culture_&_values': regex['0.0-5.0'],
                'Senior_management': regex['0.0-5.0'],
                'Work/Life_balance': regex['0.0-5.0'],
                'Pros': regex['reviews'],
                'Cons': regex['reviews'],
                'Benefits_rating': regex['0.0-5.0'],
            }
        }
        config = get_config()
        raw_dir_path = os.path.join(
            config['output_path']['main'],
            config['output_path']['raw']
        )

        cls.target_folders = raw_dir_path
        cls.target_directory_files_before = cls._get_csv_files(
            cls.target_folders)

    def setUp(self) -> None:

        # to avoid blockage from the glassdoor.com
        self._wait_for_glassdoor_server()

        return super().tearDown()

    def test_in_debug_mode(self):
        """
        Tests that data is scraped correctly in debug mode/development.

        This method creates a file using the scrape_data function 
        with debug_mode=True and checks that 
        the file is valid using the _check_if_created_file_is_valid method.
        """

        self._check_if_created_file_is_valid(
            lambda: scrape_data(jobs_number=self.jobs_number, debug_mode=True)
        )

    def test_in_production_default_job_location(self):
        """
        Tests that data is scraped correctly in normal usage.

        This method creates a file using the scrape_data function 
        with debug_mode=False and checks that 
        the file is valid using the _check_if_created_file_is_valid method.
        """

        self._check_if_created_file_is_valid(
            lambda: scrape_data(jobs_number=self.jobs_number, debug_mode=False)
        )

    def test_in_production_custom_job_location(self):
        """
        Tests that data is scraped correctly in normal usage.

        This method creates a file using the scrape_data function 
        with debug_mode=False and checks that 
        the file is valid using the _check_if_created_file_is_valid method.
        """

        self._check_if_created_file_is_valid(
            lambda: scrape_data(
                job_title="Software Engineer",
                location="Germany",
                jobs_number=self.jobs_number,
                debug_mode=False
            )
        )

    def test_in_production_no_job_in_location(self):
        """
        Tests that data is scraped correctly in normal usage.

        This method creates a file using the scrape_data function 
        with debug_mode=False and checks that 
        the file is valid using the _check_if_created_file_is_valid method.
        """
        job_title = "Pirate"
        location = "Somalia"
        jobs_number = self.jobs_number
        jobs_counter = 0
        exit_msg = "Scraping terminated before reaching target number of jobs.\n"
        f"Target number of jobs {jobs_number}, got {jobs_counter}."

        with self.assertRaisesRegex(SystemExit, exit_msg):
            scrape_data(
                job_title=job_title,
                location=location,
                jobs_number=jobs_number,
                debug_mode=False
            )

    @staticmethod
    def _wait_for_glassdoor_server():
        time_span = random.uniform(1.25, 1.7)
        sleep(time_span)

    def _check_if_created_file_is_valid(self, scrape_data_function):

        before_files = self._get_csv_files(
            self.target_folders)

        with self.assertRaises(SystemExit):
            scrape_data_function()

        after_files = self._get_csv_files(
            self.target_folders)

        difference = set(after_files) - set(before_files)

        for file in difference:
            if file not in before_files:
                self._test_csv_file_structure(file)
                break

    @staticmethod
    def _get_csv_files(directory: str) -> list[str]:

        csv_files = []

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    csv_files.append(file_path)

        return csv_files

    def _test_csv_file_structure(self, csv_file_path: str):

        delimiter = self.csv['delimiter']
        expected_values: dict[str, str] = self.csv['expected_values']

        with open(csv_file_path, newline="", encoding=self.csv['encoding']) as file:

            reader = csv.reader(file, delimiter=delimiter)
            headers = next(reader)

            self._test_each_column(expected_values, reader, headers)

    def _test_each_column(
        self,
        expected_values: dict[str, str],
        reader: _csv.reader,
            headers: list[str]
    ):

        row: list[str]
        for i, row in enumerate(reader):

            self._test_each_field(expected_values, headers, i, row)

    def _test_each_field(
            self,
            expected_values: dict[str, str],
            headers: list[str],
            i: int,
            row: list[str]
    ):

        for j, field in enumerate(row):
            header = headers[j]
            expected_regex = expected_values.get(header, None)

            if expected_regex is not None:
                assert re.match(
                    expected_regex, field), f"Invalid value in row {i+2}, column {j+1}:\
                        \nHeader :{header}:\nField  :{field}:\nExpect :{expected_regex}:"

    def tearDown(self) -> None:

        # to avoid blockage from the glassdoor.com
        self._wait_for_glassdoor_server()

        return super().tearDown()

    @classmethod
    def tearDownClass(cls):

        target_folder = cls.target_folders
        before_files = cls.target_directory_files_before

        new_files = cls._get_created_files()

        for filename in new_files:
            if filename not in before_files:
                os.remove(filename)

        super().tearDownClass()

    @classmethod
    def _get_created_files(cls):

        target_folder = cls.target_folders
        before_files = cls.target_directory_files_before
        after_files = cls._get_csv_files(target_folder)

        difference = set(after_files) - set(before_files)

        return difference


if __name__ == '__main__':
    unittest.main()

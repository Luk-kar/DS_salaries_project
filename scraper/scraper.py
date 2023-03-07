"""
The module responsible for creating RAW data format,
from queries from defined:
    - job title
    - number of offers
Additional args are:
    - driver's path for selected web browser
    - debug mode for development and debugging
Arguments could be passed from the global config data file or directly into the function.
"""
# Python
import sys
from typing import Annotated
from annotated_types import Gt

# Internal
from scraper.config.get import get_config, get_url
from scraper.jobs_to_csv.webpage_getter.webpage_getter import get_webpage
from scraper.jobs_to_csv.jobs_to_csv import save_jobs_to_csv_raw

config = get_config()


def scrape_data(
        job_title: str = config['jobs_titles']['default'],
        jobs_number: Annotated[int, Gt(0)] = config['jobs_number'],
        driver_path: str = config['driver_path'],
        debug_mode: bool = config['debug_mode']
):
    """
    Scrapes job postings from the glassdoor.com based on the given job title and number of jobs. 

    Args:
        - job_title (str, optional): The job title to search for. 
        Defaults to the value in the global config data file.

        - jobs_number (int, optional): The number of job postings to scrape. 
        Defaults to the value in the global config data file.

        - driver_path (str, optional): The path to the driver of the selected web browser. 
        Defaults to the value in the global config data file.

        - debug_mode (bool, optional): Flag to enable debug mode for development and debugging. 
        Defaults to the value in the global config data file.

    Returns:
        - None

    Raises:
        - None

    This function scrapes job postings from a webpage glassdoor.com 
    using the given job title and number of jobs. It then saves the data to a CSV file. 
    The webpage is accessed using a web driver, which is specified by the driver path. 
    Debug mode can be enabled to assist with development and debugging.

    Note that the function will exit after scraping the data and saving it to the CSV file.
    """

    url = get_url(config['url'], job_title)
    driver = get_webpage(url, debug_mode, driver_path)

    save_jobs_to_csv_raw(jobs_number, debug_mode, driver)

    sys.exit(
        f"You successfully scraped {jobs_number} postings for the job position:\n{job_title}\n")

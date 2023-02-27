'''
The module responsible for creating RAW data format,
from queries from defined:
    - job title
    - number of offers
Additional args are:
    - driver's path for selected web browser
    - debug mode for development and debugging
Arguments could be passed from the global config data file or directly into the function.
'''
# Python
import sys
from typing import Annotated
from annotated_types import Gt

# Internal
from scraper.config.get import get_config, get_url
from scraper.jobs_to_csv.webpage_getter.webpage_getter import get_webpage
from scraper.jobs_to_csv.jobs_to_csv import get_jobs_to_csv

config = get_config()


def scrape_data(
        job_title: str = config['jobs_titles']['default'],
        jobs_number: Annotated[int, Gt(0)] = config['jobs_number'],
        driver_path: str = config['driver_path'],
        debug_mode: bool = config['debug_mode']
):
    '''returns uncleaned DataFrame object from searched job title on glassdoor.com'''

    url = get_url(config['url'], job_title)
    driver = get_webpage(url, debug_mode, driver_path)

    get_jobs_to_csv(jobs_number, debug_mode, driver)

    sys.exit(
        f"You successfully scraped {jobs_number} postings for the job position:\n{job_title}")

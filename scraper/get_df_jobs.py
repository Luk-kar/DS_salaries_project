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
from typing import Annotated
from annotated_types import Gt

# Internal
from scraper.config.get import get_config, get_url
from scraper.helpers.get_webpage import get_webpage
from scraper.helpers.get_jobs import get_jobs

config = get_config()


def get_df_jobs(
        job_title: str = config["jobs_titles"]["default"],
        jobs_cap: Annotated[int, Gt(0)] = config["jobs_number"],
        driver_path: str = config["driver_path"],
        debug_mode: bool = config["debug_mode"]
):
    """returns uncleaned DataFrame object from searched job title on glassdoor.com"""

    url = get_url(config['url'], job_title)
    driver = get_webpage(url, debug_mode, driver_path)

    jobs = get_jobs(jobs_cap, debug_mode, driver)

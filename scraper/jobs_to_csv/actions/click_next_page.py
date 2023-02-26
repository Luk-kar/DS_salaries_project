# Python
import sys

# External
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

# Internal
from scraper._types import MyWebDriver
from .click_javascript import click_via_javascript


def click_next_page(driver: MyWebDriver, jobs_counter: int, jobs_number: int):
    """
    Clicks on the 'Next' button to navigate to the next page of job listings on Glassdoor.

    Args:
    - driver (MyWebDriver): The webdriver instance used to interact with the Glassdoor website.
    - jobs_counter (int): The number of jobs that have been scraped so far.
    - jobs_number (int): The total number of jobs to scrape.

    Raises:
    - ElementClickInterceptedException: If the 'Next' button is present 
    but is not clickable due to an overlay element blocking it.

    - NoSuchElementException: If the 'Next' button is not found on the page, 
    which indicates that there are no more job listings to scrape.

    Note:
    - If the 'Next' button is not clickable due to a driver's error blocking it, 
    the function will attempt to click the button using JavaScript 
    instead of the standard WebDriver click method.
    """

    try:
        next_page = driver.find_element(
            By.XPATH, "//button[@data-test='pagination-next']")

        if next_page.is_enabled():
            next_page.click()
        else:
            _exit_scraping_when_no_more_jobs(jobs_counter, jobs_number)

    except ElementClickInterceptedException:
        click_via_javascript(driver, next_page)

    except NoSuchElementException:
        _exit_scraping_when_no_more_jobs(jobs_counter, jobs_number)


def _exit_scraping_when_no_more_jobs(jobs_counter: int, jobs_number: int):
    """
    Exits the program when there is no more jobs to scrape from the website.

    Args:
    - jobs_counter (int): The number of jobs that have been scraped so far.
    - jobs_number (int): The total number of jobs to scrape.
    """

    sys.exit(
        f"Scraping terminated before reaching target number of jobs.\n\
            Needed {jobs_counter}, got {jobs_number}."
    )

'''
Module responsible for parsing HTML source code and getting values
for a given dictionary of job values.
'''
# External
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


# Internal
from scraper._types import Job_elements
from scraper.jobs_to_csv.elements_query.XPATH_text_getter import get_XPATH_values


def get_values_from_element(source_html: WebElement, job_values: Job_elements):
    '''get values from a source web element for an each web element in the job values'''

    for values in job_values.values():
        try:

            values.value = get_XPATH_values(source_html, values)

        except NoSuchElementException:
            pass

    return job_values

'''
Module responsible for parsing HTML source code and getting values
for a given dictionary of job values.
'''
# External
from selenium.common.exceptions import NoSuchElementException


# Internal
from scraper._types import MyWebElement, Job_elements
from scraper.helpers.get_one_job.get_XPATH_text import get_XPATH_text


def get_values_from_source(source_html: MyWebElement, job_values: Job_elements):
    '''get values from a source web element for an each web element in the job values'''

    for values in job_values.values():
        try:
            values['value'] = get_XPATH_text(
                source_html, values['element'], values["is_list"])
        except NoSuchElementException:
            pass

    return job_values

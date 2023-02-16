
# External
from selenium.common.exceptions import NoSuchElementException


# Internal
from _types import DriverChrome
from scraper.helpers.get_XPATH_text import get_XPATH_text


def get_values_from_source(source_html: DriverChrome, job_values):
    '''get values from a source element for an each element in the dict'''

    for values in job_values.values():
        try:
            values['value'] = get_XPATH_text(
                source_html, values['element'], values["is_list"])
        except NoSuchElementException:
            pass

    return job_values

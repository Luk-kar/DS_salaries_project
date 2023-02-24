
'''
This module provides a function that returns the text of a selected element
or elements using an XPath query on a web page, with the option to return a list of texts and
a fallback "NA_value" from the configuration file.
'''
# External
from selenium.webdriver.common.by import By

# Internal
from scraper._types import MyWebElement
from scraper.config.get import get_config

config = get_config()
Elements = list[MyWebElement]


def get_XPATH_values(source_html: MyWebElement, search: XpathSearch) -> list | str:
    '''return text or texts of selected web element'''

    if isinstance(search, XpathListSearch):

        elements: Elements = source_html.find_elements(
            By.XPATH, element
        )

        texts: list[str] = []
        for elem in elements:
            texts.append(elem.text)

        return texts

    else:

        text: str = source_html.find_element(
            By.XPATH, element
        ).text

        return text


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
na_value = config["NA_value"]
Elements = list[MyWebElement]


class XpathSearch:
    def __init__(self, element: str):
        self.value = na_value
        self.element = element


class XpathListSearch(XpathSearch):
    pass


def get_XPATH_values(source_html: MyWebElement, search: XpathSearch | XpathListSearch) -> list | str:
    '''return text or texts of selected web element'''

    if isinstance(search, XpathListSearch):

        elements: Elements = source_html.find_elements(
            By.XPATH, search.element
        )

        texts = _get_all_texts(elements)

        return texts

    else:

        text: str = _get_text(source_html, search)

        return text


def _get_all_texts(elements):

    texts: list[str] = []
    for elem in elements:
        texts.append(elem.text)
    return texts


def _get_text(source_html, search):
    return source_html.find_element(
        By.XPATH, search.element
    ).text

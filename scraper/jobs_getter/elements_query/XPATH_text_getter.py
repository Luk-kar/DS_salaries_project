"""
This module provides a function that returns the text of a selected element
or elements using an XPath query on a web page, with the option to return a list of texts and
a fallback "NA_value" from the configuration file.
"""

# External
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# Internal
from scraper.config.get import get_config
from scraper.config._types import NA_value

config = get_config()
na_value = config["NA_value"]

WebElements = list[WebElement]


class XpathSearch:
    """
    A class representing an XPath search.

    Args:
    - element (str): an XPath query string for the desired element.
    """

    def __init__(self, element: str):
        self.value: NA_value | str | list[str] = na_value
        self.element = element


class XpathListSearch(XpathSearch):
    """
    A class representing an XPath search that returns a list of elements.
    """
    pass


def get_XPATH_values(
        source_html: WebElement,
        search: XpathSearch | XpathListSearch
) -> list | str:
    """
    Extracts the text or texts of selected web element.

    Args:
    - source_html (WebElement): the web page element to search.
    - search (XpathSearch or XpathListSearch): a class representing 
    an XPath query for the desired element(s).

    Returns:
    - str or list[str]: the text or texts of the selected web element(s).
    """

    if isinstance(search, XpathListSearch):

        elements: WebElements = source_html.find_elements(
            By.XPATH, search.element
        )

        texts = _get_all_texts(elements)

        return texts

    else:

        text: str = _get_text(source_html, search)

        return text


def _get_all_texts(elements: WebElements) -> list[str]:
    """
    Extracts the text of a list of web elements.

    Args:
    - elements: a list of web elements.

    Returns:
    - list[str]: a list of the text of the input web elements.
    """
    texts: list[str] = []
    for elem in elements:
        texts.append(elem.text)
    return texts


def _get_text(
        source_html: WebElement,
        search: XpathSearch
) -> str:
    """
    Extracts the text of a single web element.

    Args:
    - source_html (WebElement): the web page element to search.
    - search (XpathSearch): a class representing an XPath query for the desired element.

    Returns:
    - str: the text of the selected web element.
    """
    return source_html.find_element(
        By.XPATH, search.element
    ).text

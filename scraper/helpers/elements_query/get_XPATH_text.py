
'''
This module provides a function that returns the text of a selected element
or elements using an XPath query on a web page, with the option to return a list of texts and
a fallback "NA_value" from the configuration file.
'''
# External
from selenium.webdriver.common.by import By

# Internal
from scraper._types import MyWebElement, Field_value
from scraper.config.get import get_config

config = get_config()
Elements = list[MyWebElement]


def get_XPATH_values(source_html: MyWebElement, element: str, return_list=False) -> Field_value:
    '''return text or texts of selected web element'''

    if return_list:

        elements: Elements = source_html.find_elements(
            By.XPATH, element
        )

        texts: list[str] = []
        for elem in elements:
            texts.append(elem.text)

        if not texts:
            return config["NA_value"]
        else:
            return texts

    text: str = source_html.find_element(
        By.XPATH, element
    ).text

    # todo below move to cleaning
    if \
       text == "N/A" \
       or len(text.strip()) == 0:

        text = config["NA_value"]

    else:
        text

    return text

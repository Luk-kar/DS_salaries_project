
# External
from selenium.webdriver.common.by import By

# Internal
from scraper._types import DriverChrome
from scraper.config.get import get_config

config = get_config()


def get_XPATH_text(source_html: DriverChrome, element: str, return_list=False):
    '''return text or texts of selected element'''

    if return_list:

        elements = source_html.find_elements(
            By.XPATH, element
        )

        texts: dict[str] = []
        for elem in elements:
            texts.append(elem.text)

        if not texts:
            texts = config["NA_value"]

        return texts

    text: str = source_html.find_element(
        By.XPATH, element
    ).text

    text = config["NA_value"] if text == "N/A" or len(
        text.strip()) == 0 else text

    return text


# External
from selenium.common.exceptions import (
    WebDriverException,
)
import requests

# Internal
from scraper._types import WebDriver
from scraper.config.get import get_config
from scraper.config._types import DebugMode
from scraper.helpers.get_driver import get_driver

config = get_config()


def get_webpage(url: str, debug_mode: DebugMode, driver_path: str = config["driver_path"]) -> WebDriver:
    """returns browser driver"""

    driver: WebDriver = get_driver(debug_mode, driver_path)
    try:
        driver.get(url)
    except WebDriverException as error:
        status_code = requests.get(url, timeout=3).status_code
        print(
            f"Failed to upload the url: {error}\n Status code: {status_code}")

    return driver

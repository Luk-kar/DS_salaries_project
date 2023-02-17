"""
This module provides functions for loading configuration and URL data from a YAML file and returning it in a structured format, 
including the get_config() function which returns a Config object and the get_url() function which returns a HTTP string. 
It imports the yaml library and uses the SafeLoader to safely load the YAML data.
"""
# Python
import yaml
from yaml.loader import SafeLoader

# Internal
from scraper.config._types import Config, Url, JobDefault


def get_config(path: str = 'scraper\\config\\data.yaml') -> Config:
    """It loads configuration data from a YAML file and returns it as a Config object"""

    with open(path, encoding="utf-8") as file:
        return yaml.load(file, Loader=SafeLoader)


def get_url(url: Url, job_title: JobDefault) -> str:
    """It loads url data from a YAML file and returns it as a HTTP string"""

    url: Url = url
    job_title: JobDefault = job_title

    http = url["001_base"] + job_title + \
        url["002_keyword"] + job_title + \
        url["003_location"]

    return http

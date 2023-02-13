"""
The get_args method in this module loads configuration data from a YAML file 
and returns it as a Config object.
The default file path is config\\data.yaml, 
but it can be changed by passing a different file path as an argument.
"""
# Python
import yaml
from yaml.loader import SafeLoader

# Internal
from config._types import Config, Url, JobDefault


def get_config(path: str = 'config\\data.yaml') -> Config:
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

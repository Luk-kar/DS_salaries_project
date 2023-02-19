"""
This module provides functions for loading configuration and URL data 
from a YAML file and returning it in a structured format, 
including the get_config() function which returns a Config object 
and the get_url() function which returns a HTTP string. 
It imports the yaml library and uses the SafeLoader to safely load the YAML data.
"""
# Python
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
import os
import platform

# External
from pathvalidate import sanitize_filepath

# Internal
from scraper.config._types import Config, Url, JobDefault


def get_config(path: str = 'scraper\\config\\data.yaml') -> Config:
    """It loads configuration data from a YAML file and returns it as a Config object"""

    with open(path, encoding="utf-8") as file:
        return yaml.load(file, Loader=SafeLoader)


def get_url(url: Url, job_title: JobDefault) -> str:
    """It loads url data from a YAML file and returns it as a HTTP string"""

    http = url["001_base"] + job_title + \
        url["002_keyword"] + job_title + \
        url["003_location"]

    return http


config = get_config()


def get_path_csv(directory_type: str,
                 job_title: str = config["jobs_titles"]["default"],
                 extension: str = "csv"
                 ) -> str:

    directory_main = config['output_path']['main']
    directory_target = os.path.join(directory_main, directory_type)
    jobs_title = job_title.replace(" ", "_")
    jobs_title = my_sanitize_filepath(jobs_title)
    date = datetime.now().strftime("%d-%m-%Y_%H-%M")

    database_file = f"{jobs_title}_{date}.{extension}"

    csv_file_target = os.path.abspath(
        os.path.join(directory_target, database_file))

    if is_possible_path(csv_file_target):
        return csv_file_target
    else:
        raise OSError(f"Wrong file path:\n{csv_file_target}")


def get_path_csv_raw():
    return get_path_csv(config["output_path"]["raw"])


def get_path_csv_clean():
    return get_path_csv(config["output_path"]["clean"])


def is_possible_path(file_path: str):

    # https://stackoverflow.com/a/67119769/12490791
    is_possible = file_path == my_sanitize_filepath(file_path)

    if os.path.exists(file_path) or is_possible:
        return True
    else:
        return False


def my_sanitize_filepath(path: str) -> str:
    return sanitize_filepath(
        path, platform=platform.system())

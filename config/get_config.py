"""
The get_args method in this module loads configuration data from a YAML file 
and returns it as a Config object.
The default file path is config\\data.yaml, 
but it can be changed by passing a different file path as an argument.
"""

import yaml
from yaml.loader import SafeLoader
from config.types import Config


def get_args(path: str = 'config\\data.yaml') -> Config:
    """It loads configuration data from a YAML file and returns it as a Config object"""

    with open(path, encoding="utf-8") as file:
        return yaml.load(file, Loader=SafeLoader)

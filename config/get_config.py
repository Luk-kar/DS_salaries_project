import yaml
from yaml.loader import SafeLoader
from config.Types import Config


def get_args(path: str = 'config\\data.yaml') -> Config:
    with open(path) as f:
        return yaml.load(f, Loader=SafeLoader)

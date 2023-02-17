'''
This module provides type aliases for configuration values for the scraper.
'''

from typing import Annotated, Literal
from annotated_types import Gt

JobDefault = str
JobSimilar = list[str]
JobTitles = dict[str, {'default': JobDefault,  # type: ignore[valid-type, misc]
                       'similar': JobSimilar}]  # type: ignore[valid-type, index]
JobNumber = Annotated[int, Gt(0)]
Url = dict[str, str]
DriverPath = str
DebugMode = bool
NA_value = Literal[-1]
Config = dict[str, {'jobs_titles': JobTitles, 'jobs_number': JobNumber,  # type: ignore[valid-type, misc]
                    'url': Url, 'driver_path': DriverPath, 'debug_mode': DebugMode, "NA_value": NA_value}]  # type: ignore[valid-type, index]

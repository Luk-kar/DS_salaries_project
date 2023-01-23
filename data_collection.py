"""
Created on Thu Apr  2 11:47:44 2020
@author: Ken
"""

import glassdoor_scraper as gs
import pandas as pd
import pathlib
import os

path = os.path.abspath(
    str(pathlib.Path(__file__).parent.resolve()) + "\chromedriver.exe"
)
print(path)

df = gs.get_jobs('data scientist', 1000, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index=False)

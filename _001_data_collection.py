"""
This Python code imports necessary modules, retrieves configuration settings, 
and iterates through a list of countries to scrape data for job listings from a website, 
handling potential errors during the process and printing relevant information, 
ultimately indicating when the scraping for all countries has finished.
"""

# Python
import traceback
import logging

# Internal
from scraper.config.get import get_config
from scraper.scraper import scrape_data
from scraper.jobs_to_csv.debugger.printer import print_current_date_time

config = get_config()
countries = config["locations"]["others"]

for country in countries:
    try:
        scrape_data(debug_mode=False, location=country, jobs_number=900)

    except SystemExit as _exit:
        print(_exit)

    # https://stackoverflow.com/a/4992124/12490791
    except Exception as _error:
        logging.error(traceback.format_exc(_error))

# scrape_data(debug_mode=False, jobs_number=900)

print(f"\rScraping for all countries has ended.")
print_current_date_time("End")
print(countries)

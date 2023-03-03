# Glassdoor job scraper # todo

This project web scrapes the popular job listing site "Glassdoor" for information from job listings

- Functions without any authentication e.g. user sign-ins/ API tokens and keys. Users simply modifies a config file to provide:
  - A 'base url' to scrape from, based on desired job role and country.
  - A 'target job size' i.e. number of individual job listings to scrape from.
- Script scrapes:
  - Job link, role, company and job description from glassdoor job listing results.
- Information collected are accessible to users in the form of an output csv.
- Script has been tested and verified to be working as expected for a job with:
  - A target job size of < 2000 individual listings,
  - Multiple pages > 10 pages of job listing links.

## Extracted data # todo

![](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/def-3.jpg)

## Purpose # todo

1. A means of collecting unstructured data of job descriptions provided in job listings.
   - Data collected can then be analysed and visualised to generate useful insights
2. With some technical knowledge and [familiarity on how it works](https://github.com/kelvinxuande/glassdoor-scraper/blob/master/docs/README.md#how-it-works), developers can:
   - Modify the script to work for other job listing sites with similar layouts.
   - Incorporate this script into their own data science pipelines and workflows

## Prerequisites

### Set Chrome browser

To avoid the bugs like:
[9292:9976:0302/114352.788:ERROR:gpu_init.cc(523)] Passthrough is not supported, GL is disabled, ANGLE is
[51120:18300:0302/120010.546:ERROR:gpu_init.cc(523)] Passthrough is not supported, GL is disabled, ANGLE is
https://stackoverflow.com/a/67575891/12490791

## Usage

1.
2.

## Wishlist

1. Optimizing the speed of the script. Get rid of all artificial pause scripts.
2. Making the driver more stealth
3. Searching job offers by Country/State
4. Refactor the code to more of the paradigm Object Oriented Programming (OOP) approach than Functional Programming (FP).
   It's just easier to maintain.

## Wish-not-list

1. The scraping links of job offers will make things more delicate and breakable.
   The main goal of this soft is Exploratory Data Analysis (EDA).
   When looking for a job there is a much more efferent approach than using Selenium. For example by using BeautifulSoup and scraping directly on the job postings than on the jobs aggregator.

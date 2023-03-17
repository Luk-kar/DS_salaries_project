# Glassdoor job scraper

A Python script that scrapes the popular job listing site "Glassdoor" for information from job listings

The output is in form of a table in a CSV file.

It functions without any authentication e.g. user sign-ins/ API tokens and keys.

The script has been tested and verified to be working as expected for a job with a target job size of < 900 individual listing.

## Usage 🔨

```
from scraper import scrape_data

scrape_data(
    job_title: str = config['jobs_titles']['default'],
    jobs_number: int = config['jobs_number'],
    driver_path: str = config['driver_path'],
    debug_mode: bool = config['debug_mode']
)
```

## Configuration 🪓

Simply modify a config file to provide:

- `['jobs_titles']['default']` a job to scrape
- `['jobs_number']` i.e. number of individual job listings to scrape from
- `['driver_path']` is a path for your web driver used for your browser to scrape. You can set it to auto-download
- `['NA_value']` is the type of placeholder value. Recommended using just an empty string ""
- `['debug_mode']` if True is the mode useful during the development

## The data Collected 📦

Script scrapes:

- Strings values
  - A text
    - Company name
    - Job location
    - Job title
    - Job description
  - Categorical data
    - Type of Ownership
    - The sector of the company e.g. "Education" (the industry is part of it)
    - The industry of the company e.g. "Primary & Secondary Schools" (it is part of the sector)
  - A list: Employees' notes about the company
    - Pros
    - Cons
    - Benefits reviews
- Boolean values
  - Easy application (True) or via the company's page (False)
- Numerical values
  - 0.00 - 1.00
    - Recommend to a friend
    - CEO approval
  - 1.0 - 5.0
    - Company rating
    - Career opportunities
    - Compensation & benefits
    - Culture & Values
    - Senior management
    - Work/Life_balance
    - Benefits rating
  - 0 / 0.00 - ∞
    - Salary (per hour/per year)
    - The year the company was founded
  - 24h - 30d+
    - The age of the job posting
  - Categorical data
    - The number of employees in the company
    - Revenue in USD

## Purpose 🧭

Scraping data for Exploratory data analysis (EDA) for conditions and requirements for a chosen career path. In that case data engineer.

## Prerequisites 🧰

Look at:

- [requirements.txt](scraper/requirements.txt)
- [Piffle](Piffle)

## Running the tests 🧪

To run tests, write down in the terminal, in the program folder:
`python -m unittest`
or
`scripts\run_tests.bat`

## Wish-list ✨

1. Optimizing the speed of the script. Get rid of all artificial pause scripts.
2. Making the driver more stealth
3. Searching job offers by Country/State
4. Refactor the code to more of the paradigm Object Oriented Programming (OOP) approach than Functional Programming (FP).
   It's just easier to maintain in the long term.
5. Add log errors to a file `errors.log`.
6. Add not crushing `"headless"` mode for the Chrome driver for daily usage (`debug_mode=false`)

## Non-wish-list and troubleshoots 🔥

1. No links to a job offer:
   Scraping links for job offers can make things more delicate and breakable.
   The links are displayed in a separate pop-up on the page, and you cannot be sure that they will load properly.
   The main goal of this script is exploratory data analysis (EDA).
   If you are looking for a job, there is a much more efficient approach than using Selenium.
   For example, you can use BeautifulSoup to scrape job postings directly without the browser, rather than using a job aggregator on the page with a web driver.
2. The cap is set at 900 jobs (note that this number may be outdated when you read this):
   One of the reasons why I use implementation through the main aggregation page is that it provides information on how old the job posting is, which is not directly available on the job posting itself.
3. Not sure if the job postings are picked at random, by the glassdoor search engine.
   Even when the population sample is sizeable, there is still room for bias.
4. There seem to be repeating job postings (multiplicities). But maybe the same job postings are posted more than once by the same company.
5. Sometimes you got the error:
   `Message: unknown error: cannot determine loading status`
   Long story short it means that you should reload the script. Glassdoor likes to block IP which behaves "unhuman".
6. Due to A/B tests and many possible format varieties/changes of salary data, it is not advised to do parsing it in the runtime.
7. In CSV files empty `na_values` are values that were not found and they are optional.
   If there are no values in the job description or button, then a corresponding error is raised.

## License 📜

Look at:

- [LICENSE](scraper/LICENSE)

## Authors 👍

- Karol Łukaszczyk - [Lukkar](https://github.com/Luk-kar)

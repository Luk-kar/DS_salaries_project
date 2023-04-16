# Glassdoor job scraper

A Python script that scrapes the popular job listing site "Glassdoor" for information from job listings

The output is in form of a table in a CSV file.

It functions without any authentication e.g. user sign-ins/ API tokens and keys.

The script has been tested and verified to be working as expected for a job with a target job size of < 900 individual listings.

It is advised to use VPN during running the script.

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
- `['locations']['default']` a place to look in
- `['jobs_number']` i.e. number of individual job listings to scrape from
- `['driver_path']` is a path for your web driver used for your browser to scrape. You can set it to auto-download
- `['NA_value']` is the type of placeholder value. Recommended using just an empty string ""
- `['debug_mode']` if True is the mode useful during the development

## The data collected 📦

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

Scraping data for Exploratory data analysis (EDA) for conditions and requirements for a chosen career path. In that case: **data engineer**.

## Prerequisites 🧰

Look at:

- [requirements.txt](scraper/requirements.txt)
- [Piffle](Piffle)

## Running the tests 🧪

On Windows `Run as Administrator` to avoid a bug:<br>
`PermissionError: [WinError 5] Access is denied`

To run tests, write down in the terminal, in the program's folder: <br>
`python -m unittest`<br>
or<br>
`scripts\run_tests.bat`<br>
or if selected file:<br>
`python -m unittest discover -s test -p "test_webdriver.py"`<br>
or selected class in the file:<br>
`python -m unittest discover -s test -p "test_webdriver.py" -k TestJobValueGetterFunctions`<br>
or selected test in the class:<br>
`python -m unittest test.test_webdriver.TestJobValueGetterFunctions.test_add_values`

## Wish-list ✨

1. Optimizing the speed of the script. Get rid of the need for all artificial `pause` functions.
2. Making the driver more stealthy.
3. Refactor the code to more of the paradigm Object Oriented Programming (OOP) approach than Functional Programming (FP).
   It's just easier to maintain in the long term.
4. Add log errors to a file `errors.log`.
5. Add not crushing `"headless"` mode for the Chrome driver for production usage (`debug_mode=false`).
6. Do multithreading for many countries, and jobs. Keep in mind that it probably has to be done by many different IPs, to avoid bot detection and therefore blockage. Also, it helps to speed up scraping by not allowing glassdoor to trim your connection bandwidth down when there are too many requests on your side.
7. Do not save the result if the job posting is a duplicate.

## Non-wish-list and troubleshoots, and as intended 🔥

1. No links to a job offer:
   Scraping links for job offers can make things more delicate and breakable.
   The links are displayed in a separate pop-up on the page, and you cannot be sure that they will load properly.
   The main goal of this script is exploratory data analysis (EDA).
   If you are looking for a job, there is a much more efficient approach than using Selenium.
   For example, you can use BeautifulSoup to scrape job postings directly without using the browser,
   rather than using a job aggregator on the page.
2. The cap is set at 900 jobs _(note that this number may be outdated when you read this)_:
   One of the reasons why I use implementation through the main aggregation page is that it provides information on how old the job posting is,
   which is not directly available on the job posting itself.
3. Not sure if the job postings are picked at random, by the glassdoor search engine.
   Even when the population sample is sizeable, there is still room for bias.
4. Overall glassdoor has some issues with duplicates. Not sure how this issue could be solved _(Maybe it is anti-bot protection )_. What I know I'm not the only one having this problem:<br>
   [stackoverflow - scraping glassdoor returns duplicate entries](https://stackoverflow.com/questions/74193851/)
5. Some job postings could be fake (ghost jobs).
6. When there are a few results glassdoor gives, job matches with low resembles.<br>
   E.g. `"Data Engineer"` -> `Android Mobile Developer`
7. Sometimes you got the error:<br>
   `Message: unknown error: cannot determine loading status`<br>
   Long story short it means that you should reload the script. Glassdoor likes to block IP which behaves as "unhuman".
8. Due to A/B tests and many possible format varieties/changes of salary data, it is not advised to do parsing it in the runtime.
9. In CSV files `na_values` is a value that is empty, was not found, and is optional.
10. As mentioned previously, if there are no values in the job description or button, then a corresponding error is raised. Those values should be on each job posting.
11. When using Chrome you could have the following error:<br>
    `Passthrough is not supported, GL is disabled`<br>
    From my experience you shouldn't worry about that too much.
12. When downloading en masse, there is quite a chance that some countries could be not downloaded.

## License 📜

Look at:

- [LICENSE](scraper/LICENSE)

## Authors 👍

- Karol Łukaszczyk - [Lukkar](https://github.com/Luk-kar)

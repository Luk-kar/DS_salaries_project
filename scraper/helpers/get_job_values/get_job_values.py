'''
The Module is responsible for getting all values from a single job posting
'''
# External
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Internal
from scraper._types import MyWebElement, Job_elements, Job_values, MyWebDriver
from scraper.helpers.get_job_values.add_values_from_dict import add_values_from_dict
from scraper.helpers.get_job_values.add_values_from_element import add_values_from_element
from scraper.helpers.elements_query.await_element import await_element
from scraper.helpers.actions.pause import pause
from scraper.helpers.elements_query.get_XPATH_text import XpathListSearch, XpathSearch


def get_job_values(driver: MyWebDriver, job_button: MyWebElement) -> dict:
    '''
    Get columns values from the current selected job posting.

    Args:
    - debug_mode (bool):
        Whether or not to print debugging output
    - driver (MyWebDriver):
        The browser driver
    - job_button (MyWebDriver):
        The job button

    Returns:
    - Job_values (dict):
        A dictionary containing columns values from the job posting
    '''

    job: Job_values = {}

    job_post = await_element(
        driver, 10, By.ID, 'JDCol')

    pause()

    # Those HTML components should be on job the post
    get_job_descriptions_values(job, job_post)
    get_job_button_values(job, job_button)

    # Those HTML components are optional on job the post
    get_company_description(job, job_post)
    get_company_ratings(job, job_post)
    get_company_reviews_by_job_title(job, job_post)
    get_company_benefits_review(job, job_post)

    return job


def get_company_benefits_review(job: Job_values, job_post: MyWebElement):
    '''
    Updates the passed job dictionary dictionary with reviews
    company's benefits and their overall score.

    The company benefits element is optional.
    If some values don't exist,
    they will be updated with the `NA_value` from the `config` file.

    Args:
    - job (dict): A dictionary containing job details.
    - job_post (MyWebDriver): The web page source for a job.

    Returns:
    - None
    '''

    benefits_review: Job_elements = {

        "Benefits_rating": XpathSearch(
            '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div//div[@class="ratingNum mr-sm"]'
        ),
        "Benefits_rating": XpathListSearch(
            '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div'
        ),
    }

    try:
        add_values_from_element(
            job,
            job_post, benefits_review
        )

    except NoSuchElementException:
        add_values_from_dict(job, benefits_review)


def get_company_reviews_by_job_title(job: Job_values, job_post: MyWebElement):
    '''
    Updates the passed job dictionary dictionary with reviews
    (Pros and Cons) of the company based on the job title. 

    The company reviews by job title element is optional.
    If some values don't exist,
    they will be updated with the `NA_value` from the `config` file.

    Args:
    - job (dict): A dictionary containing job details.
    - job_post (MyWebDriver): The web page source for a job.

    Returns:https://github.com/Luk-kar/DS_salaries_project/pull/1/files
    - None.
    '''

    reviews_by_job_title: Job_elements = {
        "Pros": XpathListSearch(
            './/*[text() = "Pros"]//parent::div//*[contains(name(), "p")]'
        ),
        "Cons": XpathListSearch(
            './/*[text() = "Cons"]//parent::div//*[contains(name(), "p")]'
        ),
    }

    try:
        reviews_info: MyWebElement = job_post.find_element(
            By.ID, "Reviews"
        )

        add_values_from_element(
            job,
            reviews_info, reviews_by_job_title
        )

    except NoSuchElementException:
        add_values_from_dict(
            job,
            reviews_by_job_title
        )


def get_company_ratings(job: Job_values, job_post: MyWebElement):
    '''
    Updates the passed job dictionary with the company rating values
    scraped from the job posting element.

    The company rating element is optional.
    If some values don't exist,
    they will be updated with the `NA_value` from the `config` file.

    Args:
    - job (dict): A dictionary containing job details.
    - job_post (MyWebDriver): The web page source for a job.

    Returns:
        - None.
    '''

    rating_description: Job_elements = {

        "Friend_recommend": XpathSearch(
            './/div[@class="css-ztsow4"]'
        ),
        "CEO_approval": XpathSearch(
            './/div[@class="css-ztsow4 ceoApprove"]'
        ),
        "Career_Opportunities": XpathSearch(
            './/*[text() = "Career Opportunities"]/following-sibling::span[2]'
        ),
        "Comp_&_Benefits": XpathSearch(
            './/*[text() = "Comp & Benefits"]/following-sibling::span[2]'
        ),
        "Culture_&_Values": XpathSearch(
            './/*[text() = "Culture & Values"]/following-sibling::span[2]'
        ),
        "Senior_Management": XpathSearch(
            './/*[text() = "Senior Management"]/following-sibling::span[2]'
        ),
        "Work/Life_Balance": XpathSearch(
            './/*[text() = "Work/Life_Balance"]/following-sibling::span[2]'
        ),
    }

    try:
        rating_info: MyWebElement = job_post.find_element(
            By.XPATH, '//div[@data-test="company-ratings"]'
        )

        add_values_from_element(
            job,
            rating_info, rating_description
        )

    except NoSuchElementException:
        add_values_from_dict(
            job,
            rating_description
        )


def get_company_description(job: Job_values, job_post: MyWebElement):
    '''
    Updates the passed job dictionary with the company description values
    scraped from the job posting element.

    The company description element is optional.
    If some values don't exist,
    they will be updated with the `NA_value` from the `config` file.

    Args:
    - job (dict): A dictionary containing job details.
    - job_post (MyWebDriver): The web page source for a job.

    Returns:
        - None.
    '''

    company_description: Job_elements = {

        "Employees": XpathSearch(
            './/div//*[text() = "Size"]//following-sibling::*'
        ),
        "Type_of_ownership": XpathSearch(
            './/div//*[text() = "Type"]//following-sibling::*'
        ),
        "Sector": XpathSearch(
            './/div//*[text() = "Sector"]//following-sibling::*'
        ),
        "Founded": XpathSearch(
            './/div//*[text() = "Founded"]//following-sibling::*'
        ),
        "Industry": XpathSearch(
            './/div//*[text() = "Industry"]//following-sibling::*'
        ),
        "Revenue_USD": XpathSearch(
            './/div//*[text() = "Revenue"]//following-sibling::*'
        ),
    }

    try:
        company_info: MyWebElement = job_post.find_element(
            By.ID, "EmpBasicInfo")

        add_values_from_element(
            job,
            company_info, company_description
        )

    except NoSuchElementException:
        add_values_from_dict(
            job,
            company_description
        )


def get_job_button_values(job: Job_values, job_button: MyWebElement):
    '''
    Updates the passed job dictionary with the job post age and Easy apply values
    scraped from the job posting button.

    The button element should exist.
    If some values don't exist,
    they will be updated with the `NA_value` from the `config` file.

    Args:
    - job (dict): A dictionary containing job details.
    - job_post (MyWebDriver): The web page source for a job.

    Returns:
    - None
    '''

    job_button_info: Job_elements = {

        "Job_age": XpathSearch(
            './/div[@data-test="job-age"]'
        ),
        "Easy_apply": XpathSearch(
            './/div[@class="css-pxdlb2"]/div[1]'
        ),
    }

    add_values_from_element(
        job,
        job_button, job_button_info
    )


def get_job_descriptions_values(job: Job_values, job_post: MyWebElement):
    '''
    Updates the passed job dictionary with the job description values
    scraped from the job posting.

    The job description element should exist.
    If some values don't exist,
    they will be updated with the `NA_value` from the `config` file.

    Args:
    - job (dict): A dictionary containing job details.
    - job_post (MyWebDriver): The web page source for a job.

    Returns:
    - None
    '''

    job_description: Job_elements = {

        "Company_Name": XpathSearch(
            './/div[@data-test="employerName"]'
        ),
        "Rating": XpathSearch(
            './/span[@data-test="detailRating"]'
        ),
        "Location": XpathSearch(
            './/div[@data-test="location"]'
        ),
        "Job_Title": XpathSearch(
            './/div[@data-test="jobTitle"]'
        ),
        "Description": XpathSearch(
            './/div[@class="jobDescriptionContent desc"]'
        ),
        "Salary": XpathSearch(
            './/span[@data-test="detailSalary"]'
        ),
    }

    add_values_from_element(
        job,
        job_post, job_description
    )

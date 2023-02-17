
# External
from selenium.common.exceptions import (
    NoSuchElementException
)
from selenium.webdriver.common.by import By

# Internal
from scraper._types import Driver, Job_elements
from scraper.helpers.add_columns_to_row_from_dict import add_columns_to_row_from_dict
from scraper.helpers.add_columns_to_row_from_source import add_columns_to_row_from_source
from scraper.helpers.print_key_value_pairs import print_key_value_pairs
from scraper.helpers.await_element import await_element
from scraper.helpers.pause import pause
from scraper.config.get import get_config


config = get_config()


def get_one_job(debug_mode: bool, driver: Driver, job_button: Driver):
    '''get columns from current selected job description'''

    job = {}

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

    if debug_mode:
        print_key_value_pairs(job)

    return job


def get_company_benefits_review(job, job_post):

    na_value = config["NA_value"]

    benefits_review: Job_elements = {
        "Benefits_rating": {
            "value": na_value,
            "element": '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsRating")]//div//div[@class="ratingNum mr-sm"]',
            "is_list": False
        },
        "Benefits_reviews": {
            "value": na_value,
            "element": '//div[starts-with(@data-brandviews,"MODULE:n=jobs-benefitsHighlights")]/div',
            "is_list": True
        },
    }

    try:
        add_columns_to_row_from_source(
            job,
            job_post, benefits_review
        )

    except NoSuchElementException:
        add_columns_to_row_from_dict(job, benefits_review)


def get_company_reviews_by_job_title(job, job_post):

    na_value = config["NA_value"]

    reviews_by_job_title: Job_elements = {
        "Pros": {
            "value": na_value,
            "element": './/*[text() = "Pros"]//parent::div//*[contains(name(), "p")]',
            "is_list": True
        },
        "Cons": {
            "value": na_value,
            "element": './/*[text() = "Cons"]//parent::div//*[contains(name(), "p")]',
            "is_list": True
        },
    }

    try:
        reviews_info: Driver = job_post.find_element(
            By.ID, "Reviews"
        )

        add_columns_to_row_from_source(
            job,
            reviews_info, reviews_by_job_title
        )

    except NoSuchElementException:
        add_columns_to_row_from_dict(
            job,
            reviews_by_job_title
        )


def get_company_ratings(job, job_post):

    na_value = config["NA_value"]

    rating_description: Job_elements = {
        "Friend_recommend": {
            "value": na_value,
            "element": './/div[@class="css-ztsow4"]',
            "is_list": False
        },
        "CEO_approval": {
            "value": na_value,
            "element": './/div[@class="css-ztsow4 ceoApprove"]',
            "is_list": False
        },
        "Career_Opportunities": {
            "value": na_value,
            "element": './/*[text() = "Career Opportunities"]/following-sibling::span[2]',
            "is_list": False
        },
        "Comp_&_Benefits": {
            "value": na_value,
            "element": './/*[text() = "Comp & Benefits"]/following-sibling::span[2]',
            "is_list": False
        },
        "Culture_&_Values": {
            "value": na_value,
            "element": './/*[text() = "Culture & Values"]/following-sibling::span[2]',
            "is_list": False
        },
        "Senior_Management": {
            "value": na_value,
            "element": './/*[text() = "Senior Management"]/following-sibling::span[2]',
            "is_list": False
        },
        "Work/Life_Balance": {
            "value": na_value,
            "element": './/*[text() = "Work/Life_Balance"]/following-sibling::span[2]',
            "is_list": False
        },
    }

    try:
        rating_info: Driver = job_post.find_element(
            By.XPATH, '//div[@data-test="company-ratings"]'
        )

        add_columns_to_row_from_source(
            job,
            rating_info, rating_description
        )

    except NoSuchElementException:
        add_columns_to_row_from_dict(
            job,
            rating_description
        )


def get_company_description(job, job_post):

    na_value = config["NA_value"]

    company_description: Job_elements = {
        "Size": {
            'value': na_value,
            "element": './/div//*[text() = "Size"]//following-sibling::*',
            "is_list": False
        },
        "Type_of_ownership": {
            'value': na_value,
            "element": './/div//*[text() = "Type"]//following-sibling::*',
            "is_list": False
        },
        "Sector": {
            'value': na_value,
            "element": './/div//*[text() = "Sector"]//following-sibling::*',
            "is_list": False
        },
        "Founded": {
            'value': na_value,
            "element": './/div//*[text() = "Founded"]//following-sibling::*',
            "is_list": False
        },
        "Industry": {
            'value': na_value,
            "element": './/div//*[text() = "Industry"]//following-sibling::*',
            "is_list": False
        },
        "Revenue": {
            'value': na_value,
            "element": './/div//*[text() = "Revenue"]//following-sibling::*',
            "is_list": False
        },
    }

    try:
        company_info = job_post.find_element(By.ID, "EmpBasicInfo")

        add_columns_to_row_from_source(
            job,
            company_info, company_description
        )

    except NoSuchElementException:
        add_columns_to_row_from_dict(
            job,
            company_description
        )


def get_job_button_values(job, job_button):

    na_value = config["NA_value"]

    job_button_info = {
        "Job_age": {
            "value": na_value,
            "element": './/div[@data-test="job-age"]',
            "is_list": False
        },
        "Easy_apply": {
            "value": na_value,
            "element": './/div[@class="css-pxdlb2"]/div[1]',
            "is_list": False
        },
    }

    add_columns_to_row_from_source(
        job,
        job_button, job_button_info
    )


def get_job_descriptions_values(job, job_post):

    na_value = config["NA_value"]

    job_description: Job_elements = {
        "Company_Name": {
            "value": na_value,
            "element": './/div[@data-test="employerName"]',
            "is_list": False
        },
        "Rating": {
            "value": na_value,
            "element": './/span[@data-test="detailRating"]',
            "is_list": False
        },
        "Location":  {
            "value": na_value,
            "element": './/div[@data-test="location"]',
            "is_list": False
        },
        "Job_Title":  {
            "value": na_value,
            "element": './/div[@data-test="jobTitle"]',
            "is_list": False
        },
        "Description":  {
            "value": na_value,
            "element": './/div[@class="jobDescriptionContent desc"]',
            "is_list": False
        },
        "Salary":  {
            "value": na_value,
            "element": './/span[@data-test="detailSalary"]',
            "is_list": False
        },
    }

    add_columns_to_row_from_source(
        job,
        job_post, job_description
    )

# Data Science Salary Estimator: Project Overview

![Data processing bro](doc\images\Data-processing-bro-readme.png)

- Created a tool that estimates data science salaries (MAE ~ $ `18.6K`) to help data engineers negotiate their income when they get a job.
- Scraped circa `3000` job descriptions from Glassdoor using Python and Selenium from [32 countries](scraper\config\data.yaml) around the world.
- Engineered features from the text of each job description to quantify the value companies put on `Python`, `SQL`, `Snowflake`, `AWS`, `GPC`, `Apache Spark`, `Apache Kafka`, BI Tools (`Looker`, `Tableau`, etc...)
- Optimized `Linear`, `Lasso`, and `Random Forest Regressors` using `GridsearchCV` to reach the best model. Built a client-facing API using flask

## Code and Resources Used

**Python Version:** `3.11`

**Packages:** <br>`Pandas`, `Numpy`, `Sklearn`, `NLTK`, `Wordcloud`, `Matplotlib`, `Plotly`, `Seaborn`, `Selenium`, `Flask`, `JSON`, `Pickle`...<br>
**For Whole Project:**<br>
`pip install -r requirements.txt`<br>
**For Web Framework:** <br>
`cd FlaskAPI`, `pip install -r requirements.txt`

**[Scraper Github](scraper\README.md)**

## YouTube Project Walk-Through

The project is based on Ken Jee's repository: [PlayingNumbers](https://github.com/PlayingNumbers)

The Video Walk-Through: [Ken Jee - Data Science Project from Scratch](https://www.youtube.com/playlist?list=PL2zq7klxX5ASFejJj80ob9ZAnBHdz5O1t)

The video and the project are several years old, so keep in mind that some things could be outdated.

## Web Scraping

Tweaked the web scraper GitHub repo to scrape job postings from glassdoor.com. With each job, we got the following:

- Company_name
- Rating
- Location
- Job_title
- Description
- Job_age
- Easy_apply
- Salary
- Employees
- Type_of_ownership
- Sector
- Founded
- Industry
- Revenue_USD
- Friend_recommend
- CEO_approval
- Career_opportunities
- Comp\_&_benefits
- Culture\_&_values
- Senior_management
- Work/Life_balance
- Pros
- Cons
- Benefits_rating
- Benefits_reviews

## Data Cleaning

After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

The data extracted directly from the postings:

- Company Name
- Ratings
- Job Location
- Job Title
- Job Description
- Job Posting Age
- Easy Apply Option
- Salary Ranges (Min, Max)
- Number of Employees in the Company
- Type of Ownership
- Company Sector
- Company Industry
- Yearly Revenue in USD
- Employee Reviews

The data was enriched with additional information (based on the Job Description and the Job Title):

- Contract Type (is a time-framed contract Y\N)
- Seniority (jr, mid, senior, management)
- Education (BA, MS, Phd, Certificate)
- Version control (Git, SVN, Gitlab and other platforms)
- Cloud Platform (AWS, GPC, Azure...)
- RDBMS (MySQL, PostgresSQL...)
- Search & Analytics (Snowflake, Google BigQuery...)
- Data Integration and Processing (Databricks, Informatica PowerCenter...)
- Stream Processing Tools (Apache KAfka, Apache Flink...)
- Workflow Orchestration Tools (Apache Airflow, SSIS...)
- Big Data Processing (Apache Spark, Apache Hadoop...)
- Operating System (Windows, Linux...)
- Programming Languages (Python, SQL, Java, Scala...)
- Business Intelligence Tools (Power BI, Tableau...)
- Machine Learning Frameworks (PyTorch, TensorFlow...)

## EDA

I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights:

![Job Density](doc\images\job-density.png)
![Average Salary by Country in the World](doc\images\Average_Salary_by_Country_in_the_World.png)
![Top 10 Tech skills required](doc\images\Top-10-Tech-skills-required.png)

The EDA is in convenient format here 👉 [+100 insights - Data Engineer 🧭🗺️](https://www.kaggle.com/code/lukkardata/100-insights-data-engineer)

## Model Building

First, I removed all data without salary information. Secondly, I transformed the categorical variables into dummy variables. I also split the data into train and test sets with a test size of 20%.

I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad for this type of model.

I tried three different models:

- **Multiple Linear Regression** – Baseline for the model
- **Lasso Regression** – Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.
- **Random Forest** – Again, with the sparsity associated with the data, I thought that this would be a good fit.

## Model performance

The Random Forest model far outperformed the other approaches on the test and validation sets.

- **Random Forest** : MAE = 18.67
- **Linear Regression**: MAE = 58539069871.22 (Yikes!)
- **Ridge Regression**: MAE = 19.99

## Productionization

In this step, I built a flask API endpoint that was hosted on a local webserver by following Ken's Jee steps (I had to change a few steps because not everything was up to date). The API endpoint takes in a request from the "GET" method sending in the body values from a job listing and returns an estimated salary.

## Acknowledgments

This project was inspired by Ken Jee's work, and the author would like to extend special thanks to him.

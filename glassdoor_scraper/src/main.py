# Import necessary libraries

# standard libraries
import argparse
import csv
from datetime import datetime
import json
import os
from os.path import exists
import sys
from time import time
import urllib.parse

# 3rd-party libraries
import enlighten

# custom functions
from glassdoor_scraper.src.packages.utils import requestAndParse
from glassdoor_scraper.src.packages.listing import extract_listing
from glassdoor_scraper.src.packages.page import extract_maximums, extract_listings


class glassdoor_scraper():

    def __init__(self, configfile, baseurl, targetnum) -> None:

        # load config file configuration
        base_url, target_num = self.load_configs(path=configfile)

        # overwrite args that are not none
        if type(baseurl) != type(None):
            base_url = baseurl
            print("Using supplied baseurl")
        if type(targetnum) != type(None):
            target_num = targetnum
            print("Using supplied targetnum")
        print(configfile, baseurl, targetnum)

        # initializes output directory and file
        if not os.path.exists('data/RAW'):
            os.makedirs('data/RAW')
        now = datetime.now()  # current date and time
        output_fileName = "./data/RAW/jobs_" + \
            now.strftime("%d-%m-%Y") + ".csv"
        csv_header = [("companyName", "company_starRating", "company_offeredRole",
                       "company_roleLocation", "listing_jobDesc", "requested_url")]
        self.fileWriter(listOfTuples=csv_header,
                        output_fileName=output_fileName)

        maxJobs, maxPages = extract_maximums(base_url)
        # print("[INFO] Maximum number of jobs in range: {}, number of pages in range: {}".format(maxJobs, maxPages))
        if (target_num >= maxJobs):
            print(
                "[ERROR] Target number larger than maximum number of jobs. Exiting program...\n")
            os._exit(0)

        # initializes enlighten_manager
        enlighten_manager = enlighten.get_manager()
        progress_outer = enlighten_manager.counter(
            total=target_num, desc="Total progress", unit="listings", color="green", leave=False)

        # initialise variables
        page_index = 1
        total_listingCount = 0

        # initializes previous url as base url
        previous_url = base_url

        while total_listingCount <= target_num:

            # clean up buffer
            list_returnedTuple = []

            new_url = self.update_url(previous_url, page_index)
            page_soup, _ = requestAndParse(new_url)
            listings_set, jobCount = extract_listings(page_soup)
            progress_inner = enlighten_manager.counter(total=len(
                listings_set), desc="Listings scraped from page", unit="listings", color="blue", leave=False)

            print("\n[INFO] Processing page index {}: {}".format(
                page_index, new_url))
            print("[INFO] Found {} links in page index {}".format(
                jobCount, page_index))

            for listing_url in listings_set:

                # to implement cache here
                returned_tuple = extract_listing(listing_url)
                list_returnedTuple.append(returned_tuple)
                # print(returned_tuple)
                progress_inner.update()

            progress_inner.close()

            self.fileWriter(listOfTuples=list_returnedTuple,
                            output_fileName=output_fileName)

            # done with page, moving onto next page
            total_listingCount = total_listingCount + jobCount
            print("[INFO] Finished processing page index {}; Total number of jobs processed: {}".format(
                page_index, total_listingCount))
            page_index = page_index + 1
            previous_url = new_url
            progress_outer.update(jobCount)

        progress_outer.close()

    def load_configs(self, path):
        '''loads config file defined parameters'''

        with open(path) as config_file:
            configurations = json.load(config_file)

        base = configurations['url']["001_base"]
        keyword = configurations['url']["002_keyword"]
        job_type = configurations['url']["003_job_type"][0]
        job = configurations['jobs'][0]

        # encode job titles to url format
        job = urllib.parse.quote(job)

        base_url = base + job + keyword + job + job_type
        target_num = int(configurations["target_num"])
        return base_url, target_num

    def fileWriter(self, listOfTuples, output_fileName):
        '''
        appends list of tuples in specified output csv file
        a tuple is written as a single row in csv file
        '''
        with open(output_fileName, 'a', newline='') as out:
            csv_out = csv.writer(out)
            for row_tuple in listOfTuples:
                try:
                    csv_out.writerow(row_tuple)
                    # can also do csv_out.writerows(data) instead of the for loop
                except Exception as e:
                    print("[WARN] In filewriter: {}".format(e))

    def update_url(self, prev_url, page_index):
        '''updates url according to the page_index desired'''

        if page_index == 1:
            prev_substring = ".htm"
            new_substring = "_IP" + str(page_index) + ".htm"
        else:
            prev_substring = "_IP" + str(page_index - 1) + ".htm"
            new_substring = "_IP" + str(page_index) + ".htm"

        new_url = prev_url.replace(prev_substring, new_substring)
        return new_url


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configfile', help="Specify location of json config file",
                        type=str, required=False, default="config.json")
    parser.add_argument('-b', '--baseurl', help="Base_url to use. Overwrites config file",
                        type=str, required=False, default=None)
    parser.add_argument('-tn', '--targetnum', help="Target number to scrape. Overwrites config file",
                        type=int, required=False, default=None)
    args = vars(parser.parse_args())

    glassdoor_scraper(
        configfile=args["configfile"],
        baseurl=args["baseurl"],
        targetnum=args["targetnum"]
    )

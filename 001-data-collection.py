import argparse
from glassdoor_scraper.src.main import glassdoor_scraper

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--configfile', help="Specify location of json config file",
                    type=str, required=False, default="./glassdoor_scraper/src/config.json")
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

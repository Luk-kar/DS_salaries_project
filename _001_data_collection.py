from scraper.config.get import get_config
from scraper.scraper import scrape_data

config = get_config()
countries = config['locations']['others'][1:]

for country in countries:
    try:
        scrape_data(debug_mode=False,
                    location=country, jobs_number=900)
    except:
        pass

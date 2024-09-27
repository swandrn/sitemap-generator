import os
import sys
sys.path.append(os.getcwd())
import pandas as pd
from scraper import scrape
from storage import database
import tldextract
import time

homepage_url = 'https://www.scrapethissite.com/'
domain = tldextract.extract(homepage_url).domain

# If homepage_url exists in database and is not older than 24h:
    # Query sitemap from database
# Else run scraper:

sitemap = scrape.run_scraper(homepage_url=homepage_url, domain=domain)

landing_page_info = {
    'domain_name': [domain],
    'page_url': [homepage_url],
    'last_scraped': [int(time.time())]
}

database.nested_dict_to_df(dictionary=landing_page_info, db_name='sitemap', table_name='landing_pages')
database.flat_dict_to_sql(dictionary=sitemap, db_name='sitemap', table_name='pages_of_domain')
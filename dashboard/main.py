import os
import sys
sys.path.append(os.getcwd())
from scraper import scrape
from storage import database
import tldextract
import time
import json

homepage_url = 'https://www.scrapethissite.com/'
domain = tldextract.extract(homepage_url).domain

Session = database.create_session('sitemap')
session = Session()

timestamp = database.get_timestamp(session, url=homepage_url)
current_time = int(time.time())

if timestamp and current_time - timestamp < 86400: # If url was scraped within the last 24 hours (86400 seconds)
    # Query sitemap from database
    sitemap = database.get_sitemap(session=session, homepage_url=homepage_url)
    print(json.dumps(sitemap, indent=3))
else:
    sitemap = scrape.run_scraper(homepage_url=homepage_url, domain=domain)

    database.insert_landing_page(session=session, homepage_url=homepage_url, domain=domain, last_scraped=int(time.time()))
    database.insert_pages_of_domain(session=session, sitemap=sitemap)
    print(json.dumps(sitemap, indent=3))
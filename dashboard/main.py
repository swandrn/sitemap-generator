import os
import sys
sys.path.append(os.getcwd())
from scraper import scrape
from storage import database
import tldextract
import time
from flask import Flask
from flask import request
from urllib.parse import unquote

app = Flask(__name__)

@app.get('/generate/sitemap')
def generate_sitemap():
    # 'https://www.scrapethissite.com/'
    url = unquote(request.args.get('url'))
    domain = tldextract.extract(url).domain

    Session = database.create_session('sitemap')
    session = Session()

    timestamp = database.get_latest_timestamp(session, url=url)
    current_time = int(time.time())

    if timestamp and current_time - timestamp < 84600: # If url was scraped within the last 24 hours (86400 seconds)
        sitemap = database.get_sitemap(session=session, homepage_url=url)
    else:
        sitemap = scrape.run_scraper(homepage_url=url, domain=domain)
        database.insert_landing_page(session=session, homepage_url=url, domain=domain, last_scraped=int(time.time()))
        database.insert_pages_of_domain(session=session, sitemap=sitemap)
    return sitemap

app.run(host='localhost', port=8080)
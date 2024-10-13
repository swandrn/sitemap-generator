import os
import sys
sys.path.append(os.getcwd())
from backend.scraper import scrape
from backend.storage import database
from backend.utilities import env
import tldextract
from urllib.parse import urlparse
import time
from flask import Flask
from flask import request
from flask import render_template
from urllib.parse import unquote

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{env.SQLITE_DB_NAME}.db'
db = database.db
db.init_app(app=app)

with app.app_context():
    db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

@app.get('/generate/sitemap')
def generate_sitemap():
    # 'https://www.scrapethissite.com/'
    url = unquote(request.args.get('url'))
    subdomain_only = request.args.get('subdomain_only', default=False, type=bool)
    print(subdomain_only)
    
    domain = tldextract.extract(url).domain if subdomain_only else urlparse(url).hostname

    session = db.session

    timestamp = database.get_latest_timestamp(session, url=url)
    current_time = int(time.time())

    if timestamp and current_time - timestamp < 84600: # If url was scraped within the last 24 hours (86400 seconds)
        sitemap = database.get_sitemap(session=session, homepage_url=url)
    else:
        sitemap = scrape.run_scraper(homepage_url=url, domain=domain)
        database.insert_landing_page(session=session, homepage_url=url, domain=domain, last_scraped=int(time.time()))
        database.insert_pages_of_domain(session=session, sitemap=sitemap)
    return render_template('generate.html', sitemap=sitemap, domain=domain)

@app.get('/home')
def serve_homepage():
    return render_template('home.html', header='My Header')

app.run(host='localhost', port=8080)
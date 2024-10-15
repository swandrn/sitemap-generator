import os
import sys
sys.path.append(os.getcwd())
from backend.scraper import scrape
from backend.storage import database
from backend.utilities import env
import tldextract
from urllib.parse import urlparse
import time
import json
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
from flask import abort
from urllib.parse import unquote
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{env.SQLITE_DB_NAME}.db'
db = database.db
db.init_app(app=app)
cors = CORS()
cors.init_app(app=app)

with app.app_context():
    db.create_all()

@app.errorhandler(HTTPException)
def default_handler(e):
    err_msg = {
        'error': e.description,
        'code': e.code,
    }
    return err_msg, e.code

@app.errorhandler(404)
def page_not_found(e):
    err_msg = {
        'error': e.description,
        'code': e.code,
        }
    return err_msg, 404

@app.get('/generate/sitemap')
def generate_sitemap():
    # 'https://www.scrapethissite.com/'
    url_arg = request.args.get('url')
    if not url_arg:
        abort(404, 'Parameter url is missing')
    url = unquote(url_arg)
    subdomain_only = request.args.get('subdomain_only', default=False, type=bool)
    
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
    return jsonify(sitemap)

app.run(host='localhost', port=8080)
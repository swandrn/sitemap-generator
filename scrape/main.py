import os
import sys
sys.path.append(os.getcwd())
from utilities import paths
from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext
import json

user_profile = {}

with open(paths.PROFILE_1) as profile:
    user_profile = json.load(profile)

with sync_playwright() as p:
    browser: BrowserContext = p.firefox.launch_persistent_context(
        user_data_dir='',
        headless=False,
        screen=user_profile['headers']['screenSize'],
        user_agent=user_profile['headers']['userAgent'],
        locale=user_profile['headers']['locale'],
        accept_downloads=False,
    )
    browser.add_cookies(user_profile['cookies'])
    page = browser.new_page()
    page.goto('https://www.scrapethissite.com/')
    anchors = page.query_selector_all('a')
    links = set()
    for anchor in anchors:
        link = anchor.evaluate('(a) => a.href')
        links.add(link)
    print(links)
    #add cookies before page close
    cookies = browser.cookies()
    user_profile['cookies'] = cookies
    with open(paths.PROFILE_1, 'w') as profile:
        json.dump(user_profile, profile, indent=3)
import os
import sys
sys.path.append(os.getcwd())
from utilities import paths
from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext, Page
import json
from urllib.parse import urlparse
import tldextract

def get_all_keys(dictionary: dict):
    for key, value in dictionary.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_keys(value)

def get_all_links_to_domain(page: Page, domain: str) -> set:
    links = set()
    anchors = page.query_selector_all('a')
    for anchor in anchors:
        if not anchor.is_visible():
            continue
        link: str = anchor.evaluate('(a) => a.href')
        if not link:
            continue
        domain_of_link = urlparse(link).hostname
        if domain_of_link.find(domain) != -1:
            links.add(link)
    return links

def visit_page(page: Page, url: str, domain: str) -> set:
    try:
        page.goto(url)
    except Exception as e:
        print(f'error going to {url}: {e}')
    try:
        links = get_all_links_to_domain(page, domain)
    except Exception as e:
        print(f'error gathering links at {url}: {e}')
    return links

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
    homepage_url = 'https://www.scrapethissite.com/'
    # homepage_url = 'https://www.barstoolsports.com/'
    # Extract domain name without subdomain and suffix
    domain = tldextract.extract(homepage_url).domain
    # if not domain:
    #     # Raise some type of 'domain can't be determined' Exception
    page.goto(homepage_url)

    links = set()
    visited_links = set()
    sitemap = {}

    links.update(get_all_links_to_domain(page, domain))

    while visited_links != links:
        for link in sorted(links):
            if link in visited_links:
                continue
            nested_links = visit_page(page=page, url=link, domain=domain)
            sitemap[link] = None
            if nested_links:
                if link in nested_links:
                    nested_links.discard(link)
                sitemap[link] = dict.fromkeys(nested_links, None)
            visited_links.add(link)
            
        links.update(get_all_keys(sitemap))

    print(json.dumps(sitemap, indent=3))
    print(sorted(links))
    print(sorted(visited_links))
        
    # Add cookies before page close
    cookies = browser.cookies()
    user_profile['cookies'] = cookies
    with open(paths.PROFILE_1, 'w') as profile:
        json.dump(user_profile, profile, indent=3)
import os
import sys
sys.path.append(os.getcwd())
from utilities import paths
from playwright.sync_api import sync_playwright
from playwright.sync_api import BrowserContext, Page
import json
from urllib.parse import urlparse
import tldextract

def create_directory_structure(sitemap: dict) -> list:
    dirs_list = []
    tmp_list = []

    for k, v in sitemap.items():
        # Root of sitemap
        if v == None:
            tmp_list.append((k))
            dirs_list.append(tmp_list)
            tmp_list = []
            continue
        if not tmp_list:
            tmp_list.append((k, v))
            continue
        if tmp_list[0][1] == v:
            tmp_list.append((k, v))
        else:
            dirs_list.append(tmp_list)
            tmp_list = []
            tmp_list.append((k, v))
    dirs_list.append(tmp_list)

    return dirs_list

def get_all_keys(dictionary: dict):
    '''Get all keys of a given dictionary object'''
    for key, value in dictionary.items():
        yield key
        if isinstance(value, dict):
            yield from get_all_keys(value)

def get_all_links_to_domain(page: Page, domain: str) -> set:
    '''From the current page, create a Set of all links pointing to a page with a given domain main'''
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

def visit_page(page: Page, url: str, sitemap: dict, domain: str) -> set:
    '''Visit a page using the parent page, according to the sitemap variable, as referer'''
    try:
        referer = sitemap[url] if sitemap[url] != None else 'https://duckduckgo.com/'
        page.goto(url=url, referer=referer)
    except Exception as e:
        print(f'error going to {url} from {page.url}: {e}')
    try:
        links = get_all_links_to_domain(page, domain)
    except Exception as e:
        print(f'error gathering links at {url}: {e}')
    return links

def run_scraper(homepage_url: str, domain: str) -> dict:
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
        page.goto(homepage_url, referer='https://duckduckgo.com/')

        links = set([homepage_url])
        visited_links = set()
        sitemap = {homepage_url: None}

        links.update(get_all_links_to_domain(page, domain))

        while visited_links != links:
            for link in links:
                if link in visited_links:
                    continue
                nested_links = visit_page(page=page, url=link, sitemap=sitemap, domain=domain)
                if nested_links:
                    if sorted(nested_links) in sorted(links):
                        visited_links.add(link)
                        continue
                    if link in nested_links:
                        nested_links.discard(link)
                    for nested_link in nested_links:
                        if not nested_link in sitemap:
                            sitemap[nested_link] = link
                visited_links.add(link)
            
            links.update(get_all_keys(sitemap))

        # Add cookies before page close
        cookies = browser.cookies()
        user_profile['cookies'] = cookies
        with open(paths.PROFILE_1, 'w') as profile:
            json.dump(user_profile, profile, indent=3)
        
        return sitemap
from scraper import scrape

homepage_url = 'https://www.scrapethissite.com/'

# If homepage_url exists in database and is not older than 24h:
    # Query sitemap from database
# Else run scraper:
    # scrape.run_scraper(homepage_url=homepage_url)
import os
import sys
sys.path.append(os.getcwd())
from utilities import paths
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

user_profile = {}

with open(paths.PROFILE_2) as profile:
    user_profile = json.load(profile)

options = webdriver.FirefoxOptions()
options.add_argument(f'--width={user_profile["headers"]["screenSize"]["width"]}')
options.add_argument(f'--height={user_profile["headers"]["screenSize"]["height"]}')
options.set_preference('general.useragent.override', user_profile["headers"]["userAgent"])
driver = webdriver.Firefox(options=options)
with driver:
    driver.get('https://www.scrapethissite.com/')
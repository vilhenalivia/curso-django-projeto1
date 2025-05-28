from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

chrome_options = webdriver.ChromeOptions()
chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

browser.get('http://www.google.com.br/')
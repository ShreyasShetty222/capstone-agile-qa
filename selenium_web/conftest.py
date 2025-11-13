import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture
def driver(browser_name, headless):
    '''Create a webdriver instance for chrome or firefox. Uses webdriver-manager.
       browser_name and headless come from root conftest.'''
    browser = (browser_name or os.environ.get('BROWSER', 'chrome')).lower()
    is_headless = bool(headless) or os.environ.get('HEADLESS', 'false').lower() in ('1','true','yes')

    if browser == 'firefox':
        options = FirefoxOptions()
        if is_headless:
            options.headless = True
        # recommended CI flags for firefox (if any) can be added here
        service = FirefoxService(GeckoDriverManager().install())
        drv = webdriver.Firefox(service=service, options=options)
    else:
        # default: chrome
        options = ChromeOptions()
        # common CI flags
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        # prefer new headless if supported, fall back to classic
        if is_headless:
            try:
                options.add_argument('--headless=new')
            except Exception:
                options.add_argument('--headless')
        # remote debugging port sometimes helps
        options.add_argument('--remote-debugging-port=9222')

        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=options)

    drv.maximize_window()
    yield drv
    try:
        drv.quit()
    except Exception:
        pass
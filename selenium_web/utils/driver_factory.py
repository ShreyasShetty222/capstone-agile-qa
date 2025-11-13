import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def _is_true(val):
    return str(val).lower() in ('1','true','yes')

def create_driver(browser=None, headless=None):
    browser = (browser or os.environ.get('BROWSER') or 'chrome').lower()
    headless = True if headless is True else (_is_true(headless or os.environ.get('HEADLESS', 'false')))

    if browser == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.headless = True
        driver_path = GeckoDriverManager().install()
        # write geckodriver log for CI debugging
        service = FirefoxService(executable_path=driver_path, log_path='geckodriver.log')
        driver = webdriver.Firefox(service=service, options=options)
    else:
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-software-rasterizer')
        if headless:
            try:
                options.add_argument('--headless=new')
            except Exception:
                options.add_argument('--headless')
        # ask webdriver-manager to install a driver; capture chromedriver verbose log
        driver_path = ChromeDriverManager().install()
        service = ChromeService(executable_path=driver_path, log_path='chromedriver.log')
        driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.maximize_window()
    except Exception:
        pass
    return driver

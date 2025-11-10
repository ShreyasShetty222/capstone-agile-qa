from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
import time

# Build options (required by new Selenium/Appium)
opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"       # confirm with: adb devices
opts.set_capability("browserName", "Chrome")
# Let Appium auto-download a matching Chromedriver
opts.set_capability("appium:chromedriverAutodownload", True)

# Connect to Appium (no /wd/hub, your server has none)
driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)

try:
    driver.implicitly_wait(10)
    driver.get("https://the-internet.herokuapp.com/login")

    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]").click()

    msg = driver.find_element(By.ID, "flash").text
    print("✅ Login message:", msg)
finally:
    driver.quit()

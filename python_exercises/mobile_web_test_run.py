from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Build options
opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"  # adb devices
opts.set_capability("browserName", "Chrome")
# Auto-fetch matching Chromedriver
opts.set_capability("appium:chromedriverAutodownload", True)
# Skip Chrome first-run dialogs
opts.set_capability("goog:chromeOptions", {
    "args": ["--disable-fre", "--no-first-run", "--disable-popup-blocking"]
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)

try:
    driver.get("https://the-internet.herokuapp.com/login")

    wait = WebDriverWait(driver, 20)

    # Use CSS selectors (robust for Chrome on Android)
    user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))
    pwd  = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
    btn  = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius")))

    user.send_keys("tomsmith")
    pwd.send_keys("SuperSecretPassword!")
    btn.click()

    flash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#flash")))
    print("✅ Login message:", flash.text)
finally:
    driver.quit()

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"
opts.set_capability("browserName", "Chrome")
opts.set_capability("appium:chromedriverAutodownload", True)
opts.set_capability("acceptInsecureCerts", True)
opts.set_capability("goog:chromeOptions", {
    "args": ["--no-first-run","--disable-fre","--disable-popup-blocking",
             "--ignore-certificate-errors","--allow-insecure-localhost"]
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
wait = WebDriverWait(driver, 20)

def maybe_bypass_ssl_interstitial():
    try:
        driver.find_element(By.ID, "details-button").click()
        driver.find_element(By.ID, "proceed-link").click()
        return
    except Exception:
        pass
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys("thisisunsafe")
    except Exception:
        pass

try:
    driver.get("https://the-internet.herokuapp.com/login")
    # If SSL page appears, bypass it
    if "Your connection is not private" in driver.page_source or "chrome-error" in (driver.current_url or ""):
        maybe_bypass_ssl_interstitial()

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

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
import time

opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"
opts.set_capability("appium:appPackage", "com.android.settings")
opts.set_capability("appium:appActivity", "com.android.settings.Settings")
opts.set_capability("appium:autoGrantPermissions", True)

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
wait = WebDriverWait(driver, 25)

try:
    # Wait until the Settings app is the current package
    wait.until(lambda d: getattr(d, "current_package", "") == "com.android.settings")

    # Small pause to let UI settle
    time.sleep(1.5)

    # Scroll until something with "Network" is visible (covers "Network & internet", "Network and Internet", etc.)
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("Network")'
    )

    print("✅ Native Settings test: Found a section containing the word 'Network'.")
finally:
    driver.quit()

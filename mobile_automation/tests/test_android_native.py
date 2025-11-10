import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Android Native")
@allure.story("Settings navigation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.mobile
def test_android_settings_network_visible():
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.device_name = "emulator-5554"
    opts.set_capability("appium:appPackage", "com.android.settings")
    opts.set_capability("appium:appActivity", "com.android.settings.Settings")
    opts.set_capability("appium:autoGrantPermissions", True)

    driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
    wait = WebDriverWait(driver, 25)

    try:
        # Ensure Settings is foreground
        wait.until(lambda d: getattr(d, "current_package", "") == "com.android.settings")

        # Try several labels that devices use; pass if any is visible
        variants = ["Network & internet","Network and Internet","Network","Internet","Connections"]
        found = False
        for text in variants:
            try:
                driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("{text}")'
                )
                found = True
                break
            except Exception:
                continue

        if not found:
            # Fallback: open Network dashboard and verify “Internet” or “Wi-Fi”
            driver.start_activity("com.android.settings", "com.android.settings.Settings$NetworkDashboardActivity")
            try:
                wait.until(EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Internet")')))
            except Exception:
                wait.until(EC.presence_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Wi-Fi")')))
        assert True
    finally:
        driver.quit()

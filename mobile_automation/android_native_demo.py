from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

APK_PATH = os.path.join(os.getcwd(), "mobile_automation", "apps", "ApiDemos-debug.apk")  # change if you used another file

opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"   # adb devices
opts.set_capability("appium:app", APK_PATH)
opts.set_capability("appium:autoGrantPermissions", True)

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)

try:
    wait = WebDriverWait(driver, 20)

    # Tap "App"
    app_menu = wait.until(EC.element_to_be_clickable(
        (By.ANDROID_UIAUTOMATOR, 'new UiSelector().text("App")')
    ))
    app_menu.click()

    # Tap "Alert Dialogs"
    alert_dialogs = wait.until(EC.element_to_be_clickable(
        (By.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Alert Dialogs")')
    ))
    alert_dialogs.click()

    # Open "OK Cancel dialog with a message"
    ok_cancel = wait.until(EC.element_to_be_clickable(
        (By.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("OK Cancel")')
    ))
    ok_cancel.click()

    ok_btn = wait.until(EC.presence_of_element_located((By.ID, "android:id/button1")))
    print("✅ Native app test: OK button found:", ok_btn.text)
finally:
    driver.quit()

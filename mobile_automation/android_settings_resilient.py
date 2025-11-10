from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = UiAutomator2Options()
opts.platform_name = "Android"
opts.device_name = "emulator-5554"
opts.set_capability("appium:appPackage", "com.android.settings")
opts.set_capability("appium:appActivity", "com.android.settings.Settings")
opts.set_capability("appium:autoGrantPermissions", True)

driver = webdriver.Remote("http://127.0.0.1:4723", options=opts)
wait = WebDriverWait(driver, 25)

def try_scroll_to_any(texts):
    for t in texts:
        try:
            driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("{t}")'
            )
            return t
        except Exception:
            pass
    return None

try:
    # 1) Ensure Settings is foreground
    wait.until(lambda d: getattr(d, "current_package", "") == "com.android.settings")

    # 2) Try to find a Network-related entry with multiple variants
    target = try_scroll_to_any([
        "Network & internet",
        "Network and Internet",
        "Network",
        "Internet",
        "Connections"   # some skins use this
    ])

    if target:
        print(f"✅ Found Settings item: {target}")
    else:
        # 3) Fallback: open Network Dashboard activity directly, then verify something with 'Internet'
        driver.start_activity("com.android.settings", "com.android.settings.Settings$NetworkDashboardActivity")
        # Verify a text containing "Internet" or "Wi-Fi"
        try:
            wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Internet")')
            ))
            print("✅ Opened Network settings via activity: found 'Internet'.")
        except Exception:
            wait.until(EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Wi-Fi")')
            ))
            print("✅ Opened Network settings via activity: found 'Wi-Fi'.")

finally:
    driver.quit()

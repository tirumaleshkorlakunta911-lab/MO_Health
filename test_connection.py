from appium import webdriver
from appium.options.android import UiAutomator2Options


options = UiAutomator2Options()

options.platform_name = "Android"
options.automation_name = "UiAutomator2"

options.device_name = "47041VDJH00065"
options.udid = "47041VDJH00065"

options.app_package = "com.entrolabs.moaphealth"
options.app_activity = "com.entrolabs.moaphealth.LoginActivity"

options.no_reset = True
options.auto_grant_permissions = True

# Give Appium more time to install/start UiAutomator2
options.set_capability(
    "uiautomator2ServerInstallTimeout",
    120000,
)

options.set_capability(
    "uiautomator2ServerLaunchTimeout",
    120000,
)

options.set_capability(
    "adbExecTimeout",
    120000,
)

options.set_capability(
    "newCommandTimeout",
    300,
)


print("Connecting to Appium...")

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options,
)

print("Connected successfully!")
print("Current activity:", driver.current_activity)
print("Current package:", driver.current_package)

input(
    "MO Health is connected. "
    "Press Enter to close the session..."
)

driver.quit()

print("Session closed.")
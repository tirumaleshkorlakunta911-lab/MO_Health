import time

from appium.webdriver.common.appiumby import AppiumBy

from appium_driver import create_driver
from automation import login, select_vhc


driver = None

try:
    driver = create_driver()

    login(driver)
    print("Login successful.")

    select_vhc(driver)
    print("VHC selected.")

    time.sleep(2)

    ncd_cd = driver.find_element(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/cvncdthreeanm"
    )

    ncd_cd.click()
    print("NCD-CD clicked.")

    time.sleep(2)

    follow_up = driver.find_element(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/CVfollowup"
    )

    follow_up.click()
    print("Follow Up clicked.")

    time.sleep(3)

    print("\nActivity:")
    print(driver.current_activity)

    print("\nPackage:")
    print(driver.current_package)

    print("\n========== FOLLOW UP SCREEN ==========\n")
    print(driver.page_source)

    input(
        "\nFollow Up screen captured. "
        "Press Enter to close..."
    )

finally:
    if driver:
        driver.quit()

    print("Session closed.")
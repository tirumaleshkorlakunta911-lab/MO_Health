import time

from appium.webdriver.common.appiumby import AppiumBy

from appium_driver import create_driver
from automation import login, select_vhc


driver = None

try:
    driver = create_driver()

    # Login
    login(driver)
    print("Login successful.")

    # VHC
    select_vhc(driver)
    print("VHC selected.")

    time.sleep(2)

    # NCD-CD
    ncd_cd = driver.find_element(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/cvncdthreeanm"
    )
    ncd_cd.click()

    time.sleep(2)

    # Follow Up
    follow_up = driver.find_element(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/CVfollowup"
    )
    follow_up.click()

    time.sleep(3)

    print("\n========================================")
    print("PATIENT SEARCH SCREEN")
    print("========================================\n")

    print(driver.page_source)

    input(
        "\nPatient search screen captured. "
        "Press Enter to close..."
    )

finally:
    if driver:
        driver.quit()

    print("Session closed.")
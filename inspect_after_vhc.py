import time

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

    print("VHC selected successfully.")

    # Give the app time to load the next screen
    time.sleep(3)

    print("\n========================================")
    print("SCREEN AFTER VHC")
    print("========================================")

    print("\nPackage:")
    print(driver.current_package)

    print("\nActivity:")
    print(driver.current_activity)

    print("\nPage source:")
    print(driver.page_source)

    input(
        "\nScreen captured. "
        "Press Enter to close..."
    )

finally:

    if driver:
        driver.quit()

    print("Session closed.")
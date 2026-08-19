import time

from appium_driver import create_driver
from automation import login


driver = None

try:
    driver = create_driver()

    # Login
    login(driver)

    print("Login completed.")

    # Wait for VHC screen
    time.sleep(3)

    # Click Select VHC using the real resource ID
    select_vhc = driver.find_element(
        "id",
        "com.entrolabs.moaphealth:id/tvSelectSecretariat"
    )

    select_vhc.click()

    print("Select VHC clicked.")

    # Wait for popup/search field
    time.sleep(2)

    print("\n========================================")
    print("VHC SEARCH POPUP PAGE SOURCE")
    print("========================================\n")

    print(driver.page_source)

    input(
        "\nSearch popup captured. "
        "Press Enter to close..."
    )

finally:

    if driver:
        driver.quit()
import time

from appium_driver import create_driver
from automation import login, select_vhc

import config


driver = None

try:
    driver = create_driver()

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    login(driver)

    print("Login successful.")

    # --------------------------------------------------------
    # VHC
    # --------------------------------------------------------

    select_vhc(driver)

    print("VHC selected.")

    time.sleep(2)

    # --------------------------------------------------------
    # NCD-CD
    # --------------------------------------------------------

    ncd_cd = driver.find_element(
        "id",
        "com.entrolabs.moaphealth:id/cvncdthreeanm"
    )

    print("NCD-CD found.")

    ncd_cd.click()

    print("NCD-CD clicked.")

    time.sleep(3)

    print("\n========================================")
    print("NCD-CD SCREEN")
    print("========================================")

    print("\nPackage:")
    print(driver.current_package)

    print("\nActivity:")
    print(driver.current_activity)

    print("\nPage source:")
    print(driver.page_source)

    input(
        "\nNCD-CD screen captured. "
        "Press Enter to close..."
    )

finally:

    if driver:
        driver.quit()

    print("Session closed.")
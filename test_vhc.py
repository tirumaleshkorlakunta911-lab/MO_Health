from appium_driver import create_driver
from automation import login, select_vhc


driver = None

try:
    driver = create_driver()

    # Login
    login(driver)

    print("Login successful.")

    # Select VHC
    select_vhc(driver)

    print("VHC selection completed.")

    input(
        "\nVHC selected. "
        "Press Enter to close the session..."
    )

finally:

    if driver:
        driver.quit()

    print("Session closed.")
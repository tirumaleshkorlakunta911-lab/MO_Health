from appium_driver import create_driver

from automation import (
    login,
    select_vhc,
    wait_for_clickable,
    process_follow_up_queue_test,
)

driver = None

try:

    print("Starting MO Health automation...")

    driver = create_driver()

    print("\n[1/4] Logging in...")
    login(driver)
    print("Login successful.")

    print("\n[2/4] Selecting VHC...")
    select_vhc(driver)
    print("VHC selected.")

    print("\n[3/4] Opening NCD-CD...")
    ncd_cd = wait_for_clickable(
        driver,
        "ncd_cd",
        timeout=30,
    )
    ncd_cd.click()
    print("NCD-CD opened.")

    print("\n[4/4] Opening Follow Up...")
    follow_up = wait_for_clickable(
        driver,
        "follow_up",
        timeout=30,
    )
    follow_up.click()
    print("Follow Up opened.")

    print("\nStarting Follow Up queue...")

    patient_name = process_follow_up_queue_test(
        driver
    )


finally:

    if driver:
        driver.quit()

    print("Session closed.")
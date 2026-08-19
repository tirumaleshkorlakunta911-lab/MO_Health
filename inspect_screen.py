from appium_driver import create_driver


driver = create_driver()

try:
    print("Connected to MO Health")

    print("Current package:")
    print(driver.current_package)

    print("\nCurrent activity:")
    print(driver.current_activity)

    print("\nPage source:")
    print(driver.page_source)

    input("\nPress Enter to close...")

finally:
    driver.quit()
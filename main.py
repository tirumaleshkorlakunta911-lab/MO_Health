import automation

from appium_driver import create_driver


def main():

    driver = None

    try:

        print("=" * 60)
        print("MO HEALTH AUTOMATION")
        print("=" * 60)

        driver = create_driver()

        automation.login(
            driver
        )

        automation.select_vhc(
            driver
        )

        automation.open_ncd_cd(
            driver
        )

        automation.run(
            driver
        )

        print()
        print(
            "ALL RECORDS PROCESSED."
        )

    except Exception as error:

        print()
        print(
            "AUTOMATION FAILED:"
        )

        print(error)

        raise

    finally:

        if driver:

            try:
                driver.quit()

            except Exception:

                pass


if __name__ == "__main__":

    main()
from appium import webdriver
from appium.options.android import UiAutomator2Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


def create_driver():

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    options.device_name = config.DEVICE_NAME
    options.udid = config.UDID

    options.app_package = config.APP_PACKAGE
    options.app_activity = config.APP_ACTIVITY

    options.no_reset = True
    options.auto_grant_permissions = True

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

    options.new_command_timeout = 300

    print("Starting Appium session...")

    driver = webdriver.Remote(
        config.APPIUM_SERVER,
        options=options,
    )

    print("Appium connected.")

    return driver


def wait_element(
    driver,
    locator,
    timeout=30,
):

    return WebDriverWait(
        driver,
        timeout,
    ).until(
        EC.presence_of_element_located(
            locator
        )
    )


def wait_clickable(
    driver,
    locator,
    timeout=30,
):

    return WebDriverWait(
        driver,
        timeout,
    ).until(
        EC.element_to_be_clickable(
            locator
        )
    )
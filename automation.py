import time
import random

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

from appium_driver import (
    create_driver,
    wait_element,
    wait_clickable,
)


# ============================================================
# GENERIC WAIT HELPERS
# ============================================================

def _resolve_locator(locator_or_name):
    """
    Accept either:

        "search_field"

    or:

        (AppiumBy.ID, "some_id")
    """

    if isinstance(locator_or_name, str):
        return config.LOCATORS[locator_or_name]

    return locator_or_name


def wait_for_clickable(
    driver,
    locator_or_name,
    timeout=None,
):
    """
    Wait until an element is clickable.
    Accepts either a locator name or locator tuple.
    """

    if timeout is None:
        timeout = config.WAIT_TIMEOUT

    locator = _resolve_locator(locator_or_name)

    return WebDriverWait(
        driver,
        timeout,
    ).until(
        EC.element_to_be_clickable(locator)
    )


def wait_for_element(
    driver,
    locator_or_name,
    timeout=None,
):
    """
    Wait until an element is present.
    Accepts either a locator name or locator tuple.
    """

    if timeout is None:
        timeout = config.WAIT_TIMEOUT

    locator = _resolve_locator(locator_or_name)

    return WebDriverWait(
        driver,
        timeout,
    ).until(
        EC.presence_of_element_located(locator)
    )

# ============================================================
# SCROLLING
# ============================================================


def scroll_down(driver, duration=800):
    """
    Scroll down inside the current screen.
    """
    size = driver.get_window_size()

    width = size["width"]
    height = size["height"]

    start_x = width // 2
    start_y = int(height * 0.80)
    end_y = int(height * 0.30)

    driver.swipe(
        start_x,
        start_y,
        start_x,
        end_y,
        duration
    )

    time.sleep(1)


def scroll_up(driver, duration=800):
    """
    Scroll up inside the current screen.
    """
    size = driver.get_window_size()

    width = size["width"]
    height = size["height"]

    start_x = width // 2
    start_y = int(height * 0.30)
    end_y = int(height * 0.80)

    driver.swipe(
        start_x,
        start_y,
        start_x,
        end_y,
        duration
    )

    time.sleep(1)

def scroll_until_visible(
    driver,
    locator,
    max_scrolls=15,
    wait_after_scroll=0.15,
):
    """
    Fast element lookup.

    Searches the current screen quickly and only scrolls when
    the element is genuinely not present.
    """

    for scroll_count in range(max_scrolls + 1):

        try:
            element = WebDriverWait(
                driver,
                1.5,
                poll_frequency=0.15,
            ).until(
                EC.presence_of_element_located(locator)
            )

            if element.is_displayed():

                print(
                    f"Element found after "
                    f"{scroll_count} scroll(s)."
                )

                return element

        except Exception:
            pass

        if scroll_count >= max_scrolls:
            break

        print(
            f"Element not found. "
            f"Performing scroll #{scroll_count + 1}..."
        )

        size = driver.get_window_size()

        width = size["width"]
        height = size["height"]

        driver.swipe(
            width // 2,
            int(height * 0.75),
            width // 2,
            int(height * 0.35),
            300,
        )

        if wait_after_scroll:
            time.sleep(wait_after_scroll)

    raise RuntimeError(
        f"Could not find locator after "
        f"{max_scrolls} scroll(s): {locator}"
    )

def hide_keyboard_safely(driver):
    """
    Hide keyboard without adding a fixed 0.7 second delay.
    """

    try:
        driver.hide_keyboard()
        print("Keyboard hidden.")
    except Exception:
        pass


# ============================================================
# LOGIN
# ============================================================

def login(driver):

    print("Starting login...")

    # --------------------------------------------------------
    # Username
    # --------------------------------------------------------

    username = wait_for_element(
        driver,
        "login_username",
    )

    username.click()
    username.clear()

    username.send_keys(
        config.MO_USERNAME
    )

    print("Username entered.")

    # --------------------------------------------------------
    # Password
    # --------------------------------------------------------

    password = wait_for_element(
        driver,
        "login_password",
    )

    password.click()
    password.clear()

    password.send_keys(
        config.MO_PASSWORD
    )

    print("Password entered.")

    # --------------------------------------------------------
    # Hide keyboard
    # --------------------------------------------------------

    try:

        driver.hide_keyboard()

        print("Keyboard hidden.")

    except Exception:

        print(
            "Keyboard was already hidden."
        )

    # --------------------------------------------------------
    # Login button
    # --------------------------------------------------------

    login_button = wait_for_clickable(
        driver,
        "login_button",
    )

    login_button.click()

    print("Login button clicked.")

    return True


# ============================================================
# VHC SELECTION
# ============================================================

def select_vhc(driver):

    vhc_name = config.VHC_NAME.strip()

    if not vhc_name:

        raise ValueError(
            "VHC_NAME is not configured."
        )

    print(
        f"Selecting VHC: {vhc_name}"
    )

    # --------------------------------------------------------
    # 1. Click Select VHC
    # --------------------------------------------------------

    dropdown = wait_for_clickable(
        driver,
        "vhc_dropdown",
    )

    dropdown.click()

    print(
        "VHC dropdown opened."
    )

    # --------------------------------------------------------
    # 2. Search VHC
    # --------------------------------------------------------

    search = wait_for_element(
        driver,
        "vhc_search",
    )

    search.click()
    search.clear()

    search.send_keys(
        vhc_name
    )

    print(
        f"Searching VHC: {vhc_name}"
    )

    time.sleep(1)

    # --------------------------------------------------------
    # 3. Find exact VHC
    # --------------------------------------------------------

    exact_vhc = wait_for_element(
        driver,
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector()'
            f'.resourceId('
            f'"com.entrolabs.moaphealth:id/Tvname"'
            f')'
            f'.text("{vhc_name}")',
        ),
    )

    exact_vhc.click()

    print(
        f"VHC selected: {vhc_name}"
    )

    # --------------------------------------------------------
    # 4. Click OK
    # --------------------------------------------------------

    ok_button = wait_for_clickable(
        driver,
        "vhc_ok",
    )

    ok_button.click()

    print(
        "VHC OK button clicked."
    )

    return True


# ============================================================
# SEARCH PATIENT
# ============================================================

def search_patient(driver, patient_name):

    print("\n========== SEARCH PATIENT ==========")

    # --------------------------------------------------------
    # 1. Wait for the Follow Up search screen
    # --------------------------------------------------------

    print("Looking for patient search bar...")

    wait_for_element(
        driver,
        "search_field",
        timeout=config.WAIT_TIMEOUT,
    )

    print("Patient search bar found.")

    # --------------------------------------------------------
    # 2. Re-find the element immediately before clicking
    # --------------------------------------------------------

    search_bar = wait_for_clickable(
        driver,
        "search_field",
        timeout=config.WAIT_TIMEOUT,
    )

    search_bar.click()

    print("Patient search bar clicked.")

    # --------------------------------------------------------
    # 3. Re-find the element again
    #
    # The app may recreate searchView after focus/click.
    # --------------------------------------------------------

    search_bar = wait_for_clickable(
        driver,
        "search_field",
        timeout=config.WAIT_TIMEOUT,
    )

    # --------------------------------------------------------
    # 4. Clear existing text
    # --------------------------------------------------------

    try:
        search_bar.clear()
    except Exception:
        # SearchView may have been recreated again.
        search_bar = wait_for_clickable(
            driver,
            "search_field",
            timeout=config.WAIT_TIMEOUT,
        )

        search_bar.clear()

    # --------------------------------------------------------
    # 5. Type patient name
    # --------------------------------------------------------

    try:

        search_bar.send_keys(
            patient_name
        )

    except Exception as error:

        print(
            f"Search field changed while typing: {error}"
        )

        # Re-find the search bar one final time
        search_bar = wait_for_clickable(
            driver,
            "search_field",
            timeout=config.WAIT_TIMEOUT,
        )

        search_bar.click()
        search_bar.clear()
        search_bar.send_keys(
            patient_name
        )

    print(
        f"Patient name entered: {patient_name}"
    )

    # --------------------------------------------------------
    # 6. Wait for filtering
    # --------------------------------------------------------

    time.sleep(
        config.SEARCH_RESULT_WAIT
    )

    print(
        "Search results loaded."
    )

    print(
        "========== SEARCH PATIENT COMPLETE ==========\n"
    )

    return True


# ============================================================
# OPEN PATIENT
# ============================================================

def open_patient(
    driver,
    patient_name,
):
    """
    Find the matching patient and click View.

    The Android keyboard is hidden before clicking View
    because the keyboard can cover the patient card/button.
    """

    patient_name = patient_name.strip()

    print(
        f"Looking for patient result: {patient_name}"
    )

    # --------------------------------------------------------
    # 1. Wait for patient result
    # --------------------------------------------------------

    patient_locator = config.LOCATORS[
        "patient_name"
    ]

    patient_elements = WebDriverWait(
        driver,
        config.WAIT_TIMEOUT,
    ).until(
        EC.presence_of_all_elements_located(
            patient_locator
        )
    )

    print(
        f"Patient result elements found: "
        f"{len(patient_elements)}"
    )

    # --------------------------------------------------------
    # 2. Find matching patient
    # --------------------------------------------------------

    matching_patient = None

    for element in patient_elements:

        try:

            displayed_name = element.text.strip()

            print(
                f"Result found: {displayed_name}"
            )

            if (
                displayed_name.casefold()
                == patient_name.casefold()
            ):

                matching_patient = element

                print(
                    f"Matching patient found: "
                    f"{displayed_name}"
                )

                break

        except Exception:
            continue

    # --------------------------------------------------------
    # 3. Patient not found
    # --------------------------------------------------------

    if matching_patient is None:

        raise LookupError(
            f"Patient not found: {patient_name}"
        )

    # --------------------------------------------------------
    # 4. IMPORTANT:
    # Hide Android keyboard
    # --------------------------------------------------------

    try:

        driver.hide_keyboard()

        print(
            "Keyboard hidden."
        )

    except Exception as error:

        print(
            f"Keyboard was already hidden: {error}"
        )

    # Give the screen a moment to resize
    time.sleep(0.5)

    # --------------------------------------------------------
    # 5. Find View button
    # --------------------------------------------------------
    #
    # For now we use the View button directly.
    # The search result is already filtered to the
    # requested patient.
    # --------------------------------------------------------

    view_button = WebDriverWait(
        driver,
        config.WAIT_TIMEOUT,
    ).until(
        EC.element_to_be_clickable(
            config.LOCATORS["view_button"]
        )
    )

    print(
        "View button is visible and clickable."
    )

    # --------------------------------------------------------
    # 6. Click View
    # --------------------------------------------------------

    view_button.click()

    print(
        f"View clicked for patient: "
        f"{patient_name}"
    )

    time.sleep(2)

    print(
        "Patient form opened."
    )

    return True

def inspect_patient_form(driver):

    print("\n========== PATIENT FORM INSPECTION ==========")

    # Print current screen
    print("\n--- CURRENT SCREEN ---")

    print(driver.page_source)

    # --------------------------------------------------------
    # Find all RadioButtons
    # --------------------------------------------------------

    radio_buttons = driver.find_elements(
        AppiumBy.CLASS_NAME,
        "android.widget.RadioButton"
    )

    print(
        f"\nRadioButtons found: {len(radio_buttons)}"
    )

    for index, radio in enumerate(radio_buttons):

        print(
            f"\nRadioButton #{index}"
        )

        print(
            "text:",
            radio.get_attribute("text")
        )

        print(
            "resource-id:",
            radio.get_attribute("resourceId")
        )

        print(
            "checked:",
            radio.get_attribute("checked")
        )

        print(
            "bounds:",
            radio.get_attribute("bounds")
        )

    # --------------------------------------------------------
    # Find TextViews containing relevant words
    # --------------------------------------------------------

    text_views = driver.find_elements(
        AppiumBy.CLASS_NAME,
        "android.widget.TextView"
    )

    keywords = [
        "Diabetes",
        "Hypertension",
        "Blood Glucose",
        "Blood Pressure",
        "Sugar",
        "RBS",
        "Yes",
        "No",
        "Next",
        "Continue",
        "Submit",
    ]

    print("\n--- RELEVANT TEXT ---")

    for element in text_views:

        try:
            text = element.text.strip()

            if not text:
                continue

            if any(
                keyword.lower() in text.lower()
                for keyword in keywords
            ):
                print(
                    f"text={text!r} | "
                    f"id={element.get_attribute('resourceId')} | "
                    f"bounds={element.get_attribute('bounds')}"
                )

        except Exception:
            continue

    print(
        "\n========== END PATIENT FORM INSPECTION =========="
    )

def fill_medicine_questions(driver):

    print("\n========== MEDICINE QUESTIONS ==========")

    # ========================================================
    # QUESTION 1
    # Whether medicine taken daily → YES
    # ========================================================

    print(
        "Finding Question 1 YES..."
    )

    medicine_yes = scroll_until_visible(
        driver,
        config.LOCATORS["medicine_daily_yes"],
    )

    print(
        "Question 1 YES button found."
    )

    # Click YES
    medicine_yes.click()

    time.sleep(0.5)

    print(
        "Question 1: Whether medicine taken daily → YES"
    )

    # --------------------------------------------------------
    # Validate Question 1
    # --------------------------------------------------------

    medicine_yes = wait_for_element(
        driver,
        "medicine_daily_yes",
    )

    medicine_no = wait_for_element(
        driver,
        "medicine_daily_no",
    )

    medicine_yes_state = medicine_yes.get_attribute(
        "checked"
    )

    medicine_no_state = medicine_no.get_attribute(
        "checked"
    )

    print(
        "Question 1 YES checked:",
        medicine_yes_state
    )

    print(
        "Question 1 NO checked:",
        medicine_no_state
    )

    if medicine_yes_state != "true":

        raise RuntimeError(
            "Question 1 YES was not selected."
        )

    if medicine_no_state == "true":

        raise RuntimeError(
            "Question 1 is incorrectly selected as NO."
        )

    # ========================================================
    # QUESTION 2
    # Did the individual take today's medication
    # before coming here? → YES
    # ========================================================

    print(
        "\nFinding Question 2 YES..."
    )

    todays_yes = scroll_until_visible(
        driver,
        config.LOCATORS["before_coming_yes"],
    )

    print(
        "Question 2 YES button found."
    )

    # Click YES
    todays_yes.click()

    time.sleep(0.5)

    print(
        "Question 2: Today's medication "
        "before coming here → YES"
    )

    # --------------------------------------------------------
    # Validate Question 2
    # --------------------------------------------------------

    todays_yes = wait_for_element(
        driver,
        "before_coming_yes",
    )

    todays_no = wait_for_element(
        driver,
        "before_coming_no",
    )

    todays_yes_state = todays_yes.get_attribute(
        "checked"
    )

    todays_no_state = todays_no.get_attribute(
        "checked"
    )

    print(
        "Question 2 YES checked:",
        todays_yes_state
    )

    print(
        "Question 2 NO checked:",
        todays_no_state
    )

    if todays_yes_state != "true":

        raise RuntimeError(
            "Question 2 YES was not selected."
        )

    if todays_no_state == "true":

        raise RuntimeError(
            "Question 2 is incorrectly selected as NO."
        )

    # ========================================================
    # FINAL VALIDATION
    # ========================================================

    print(
        "\nSUCCESS: Both medicine questions are YES."
    )

    print(
        "Question 1 → YES"
    )

    print(
        "Question 2 → YES"
    )

    print(
        "========== MEDICINE QUESTIONS COMPLETE ==========\n"
    )

    return True

def detect_form_workflow(driver):

    print(
        "\n========== DETECTING FORM WORKFLOW =========="
    )

    # ========================================================
    # CONDITION 1
    #
    # "Whether diabetic" exists
    #
    # Select NO
    # Therefore patient is HYPERTENSION ONLY
    # ========================================================

    try:

        print(
            "\nChecking: Whether diabetic..."
        )

        diabetic_no = scroll_until_visible(
            driver,
            config.LOCATORS["diabetic_no"],
            max_scrolls=5,
            wait_after_scroll=0.15,
        )

        print(
            "Found: Whether diabetic"
        )

        # ----------------------------------------------------
        # Check current state
        # ----------------------------------------------------

        checked = diabetic_no.get_attribute(
            "checked"
        )

        print(
            f"Whether diabetic → NO "
            f"before click: {checked}"
        )

        # ----------------------------------------------------
        # Select NO if not already selected
        # ----------------------------------------------------

        if checked != "true":

            diabetic_no.click()

            time.sleep(0.2)

        # ----------------------------------------------------
        # Validate NO
        # ----------------------------------------------------

        checked_after = diabetic_no.get_attribute(
            "checked"
        )

        print(
            f"Whether diabetic → NO "
            f"after click: {checked_after}"
        )

        if checked_after != "true":

            raise RuntimeError(
                "Whether diabetic → NO "
                "was not selected."
            )

        print(
            "Whether diabetic → NO"
        )

        print(
            "Workflow detected: HYPERTENSION"
        )

        return "HYPERTENSION"

    except Exception as error:

        print(
            "Whether diabetic question "
            "not found."
        )


    # ========================================================
    # CONDITION 2
    #
    # "Whether hypertension" exists
    #
    # Select NO
    # Therefore patient is DIABETES ONLY
    # ========================================================

    try:

        print(
            "\nChecking: Whether hypertension..."
        )

        hypertension_no = scroll_until_visible(
            driver,
            config.LOCATORS["hypertension_no"],
            max_scrolls=5,
            wait_after_scroll=0.15,
        )

        print(
            "Found: Whether hypertension"
        )

        # ----------------------------------------------------
        # Check current state
        # ----------------------------------------------------

        checked = hypertension_no.get_attribute(
            "checked"
        )

        print(
            f"Whether hypertension → NO "
            f"before click: {checked}"
        )

        # ----------------------------------------------------
        # Select NO if not already selected
        # ----------------------------------------------------

        if checked != "true":

            hypertension_no.click()

            time.sleep(0.2)

        # ----------------------------------------------------
        # Validate NO
        # ----------------------------------------------------

        checked_after = hypertension_no.get_attribute(
            "checked"
        )

        print(
            f"Whether hypertension → NO "
            f"after click: {checked_after}"
        )

        if checked_after != "true":

            raise RuntimeError(
                "Whether hypertension → NO "
                "was not selected."
            )

        print(
            "Whether hypertension → NO"
        )

        print(
            "Workflow detected: DIABETES"
        )

        return "DIABETES"

    except Exception as error:

        print(
            "Whether hypertension question "
            "not found."
        )


    # ========================================================
    # CONDITION 3
    #
    # Neither disease question exists.
    #
    # Directly showing Measure Blood Glucose means BOTH.
    # ========================================================

    try:

        print(
            "\nChecking for Diabetes + "
            "Hypertension workflow..."
        )

        driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Measure Blood Glucose")',
        )

        print(
            "Measure Blood Glucose section found."
        )

        print(
            "No disease question found."
        )

        print(
            "Workflow detected: BOTH"
        )

        return "BOTH"

    except Exception:

        raise RuntimeError(
            "\nUnable to determine patient "
            "form workflow.\n"
            "Expected one of:\n"
            "  1. Whether diabetic → NO "
            "→ HYPERTENSION\n"
            "  2. Whether hypertension → NO "
            "→ DIABETES\n"
            "  3. Measure Blood Glucose "
            "→ BOTH"
        )

def generate_random_vitals():

    values = {
        "rbs": str(random.randint(100, 150)),
        "systolic": str(random.randint(120, 130)),
        "diastolic": str(random.randint(80, 90)),
        "pulse": str(random.randint(80, 90)),
    }

    print("\n========== GENERATED VITALS ==========")

    print(
        f"RBS       : {values['rbs']}"
    )

    print(
        f"Systolic  : {values['systolic']}"
    )

    print(
        f"Diastolic : {values['diastolic']}"
    )

    print(
        f"Pulse     : {values['pulse']}"
    )

    print(
        "======================================\n"
    )

    return values

def inspect_vital_fields(driver):

    print("\n========== VITAL FIELD INSPECTION ==========")

    # ========================================================
    # 1. FIND BLOOD GLUCOSE SECTION
    # ========================================================

    print("\nLooking for Blood Glucose...")

    blood_glucose = scroll_until_visible(
        driver,
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Blood Glucose")',
        ),
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    print("Blood Glucose section FOUND.")

    print(
        "Blood Glucose bounds:",
        blood_glucose.get_attribute("bounds"),
    )

    # --------------------------------------------------------
    # Inspect EditTexts currently around/after this section
    # --------------------------------------------------------

    edittexts = driver.find_elements(
        AppiumBy.CLASS_NAME,
        "android.widget.EditText",
    )

    print(
        f"\nEditText elements currently visible: "
        f"{len(edittexts)}"
    )

    for index, element in enumerate(edittexts):

        print(f"\nEditText #{index}")

        print(
            "resource-id:",
            element.get_attribute("resourceId"),
        )

        print(
            "hint:",
            element.get_attribute("hint"),
        )

        print(
            "text:",
            element.get_attribute("text"),
        )

        print(
            "bounds:",
            element.get_attribute("bounds"),
        )

        print(
            "displayed:",
            element.is_displayed(),
        )

    # ========================================================
    # 2. FIND BLOOD PRESSURE SECTION
    # ========================================================

    print("\nLooking for Blood Pressure...")

    blood_pressure = scroll_until_visible(
        driver,
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Blood Pressure")',
        ),
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    print("Blood Pressure section FOUND.")

    print(
        "Blood Pressure bounds:",
        blood_pressure.get_attribute("bounds"),
    )

    # --------------------------------------------------------
    # Inspect EditTexts again
    # --------------------------------------------------------

    edittexts = driver.find_elements(
        AppiumBy.CLASS_NAME,
        "android.widget.EditText",
    )

    print(
        f"\nEditText elements after Blood Pressure: "
        f"{len(edittexts)}"
    )

    for index, element in enumerate(edittexts):

        print(f"\nEditText #{index}")

        print(
            "resource-id:",
            element.get_attribute("resourceId"),
        )

        print(
            "hint:",
            element.get_attribute("hint"),
        )

        print(
            "text:",
            element.get_attribute("text"),
        )

        print(
            "bounds:",
            element.get_attribute("bounds"),
        )

        print(
            "displayed:",
            element.is_displayed(),
        )

    print(
        "\n========== END VITAL FIELD INSPECTION =========="
    )

def enter_field_value(
    driver,
    locator_name,
    value,
    max_scrolls=15,
):
    """
    Find a field, enter its value, hide the keyboard,
    and wait for the UI to settle before continuing.
    """

    print(
        f"\nLooking for field: {locator_name}"
    )

    field = scroll_until_visible(
        driver,
        config.LOCATORS[locator_name],
        max_scrolls=max_scrolls,
        wait_after_scroll=1.0,
    )

    print(
        f"Field found: {locator_name}"
    )

    # Re-find immediately before interaction.
    field = wait_for_element(
        driver,
        locator_name,
        timeout=5,
    )

    field.click()

    time.sleep(0.3)

    field.clear()

    field.send_keys(
        str(value)
    )

    print(
        f"{locator_name} entered: {value}"
    )

    # IMPORTANT:
    # Hide keyboard before searching for the next field.
    hide_keyboard_safely(driver)

    return True


def fill_rbs(driver, value):

    print("\n========== FILLING RBS ==========")

    # Find the actual RBS field directly.
    # No need to separately find Blood Glucose first.
    enter_field_value(
        driver,
        "rbs_field",
        value,
        max_scrolls=8,
    )

    print(
        "========== RBS COMPLETE ==========\n"
    )

    return True

def fill_blood_pressure(
    driver,
    systolic,
    diastolic,
    pulse,
):

    print(
        "\n========== FILLING BLOOD PRESSURE =========="
    )

    # --------------------------------------------------------
    # Find BP section once
    # --------------------------------------------------------

    scroll_until_visible(
        driver,
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Blood Pressure")',
        ),
        max_scrolls=8,
        wait_after_scroll=0.15,
    )

    print(
        "Blood Pressure section visible."
    )

    # --------------------------------------------------------
    # Find all three fields
    # --------------------------------------------------------

    systolic_field = scroll_until_visible(
        driver,
        config.LOCATORS["bp_systolic"],
        max_scrolls=3,
        wait_after_scroll=0.15,
    )

    diastolic_field = WebDriverWait(
        driver,
        2,
        poll_frequency=0.15,
    ).until(
        EC.presence_of_element_located(
            config.LOCATORS["bp_diastolic"]
        )
    )

    pulse_field = WebDriverWait(
        driver,
        2,
        poll_frequency=0.15,
    ).until(
        EC.presence_of_element_located(
            config.LOCATORS["pulse"]
        )
    )

    # --------------------------------------------------------
    # Fill systolic
    # --------------------------------------------------------

    systolic_field.click()
    systolic_field.clear()
    systolic_field.send_keys(str(systolic))

    print(
        f"bp_systolic entered: {systolic}"
    )

    # --------------------------------------------------------
    # Fill diastolic
    # --------------------------------------------------------

    diastolic_field.click()
    diastolic_field.clear()
    diastolic_field.send_keys(str(diastolic))

    print(
        f"bp_diastolic entered: {diastolic}"
    )

    # --------------------------------------------------------
    # Fill pulse
    # --------------------------------------------------------

    pulse_field.click()
    pulse_field.clear()
    pulse_field.send_keys(str(pulse))

    print(
        f"pulse entered: {pulse}"
    )

    hide_keyboard_safely(driver)

    print(
        "========== BLOOD PRESSURE COMPLETE ==========\n"
    )

    return True

def fill_vitals_by_workflow(
    driver,
    workflow,
):

    print(
        "\n========== FILLING VITALS =========="
    )

    values = generate_random_vitals()

    # ========================================================
    # DIABETES ONLY
    # ========================================================

    if workflow == "DIABETES":

        print(
            "Workflow: DIABETES"
        )

        print(
            "\nStep: Diabetes / RBS"
        )

        fill_rbs(
            driver,
            values["rbs"],
        )

    # ========================================================
    # HYPERTENSION ONLY
    # ========================================================

    elif workflow == "HYPERTENSION":

        print(
            "Workflow: HYPERTENSION"
        )

        print(
            "\nStep: Hypertension / Blood Pressure"
        )

        fill_blood_pressure(
            driver,
            values["systolic"],
            values["diastolic"],
            values["pulse"],
        )

    # ========================================================
    # BOTH
    # ========================================================

    elif workflow == "BOTH":

        print(
            "Workflow: BOTH"
        )

        print(
            "\nStep 1: Diabetes / RBS"
        )

        fill_rbs(
            driver,
            values["rbs"],
        )

        print(
            "\nStep 2: Hypertension / Blood Pressure"
        )

        fill_blood_pressure(
            driver,
            values["systolic"],
            values["diastolic"],
            values["pulse"],
        )

    else:

        raise RuntimeError(
            f"Unknown workflow: {workflow}"
        )

    print(
        "\n========== VITALS COMPLETE =========="
    )

    return values

def select_medication_options(driver):

    print(
        "\n========== MEDICATION SECTION =========="
    )

    # ========================================================
    # 1. Previous Medication → CHO
    # ========================================================

    print(
        "\nSelecting Previous Medication → CHO"
    )

    cho_option = scroll_until_visible(
        driver,
        config.LOCATORS["cho_option"],
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    cho_option.click()

    print(
        "Previous Medication → CHO selected."
    )

    time.sleep(0.5)

    hide_keyboard_safely(driver)

    # ========================================================
    # 2. Continue with current medication → YES
    # ========================================================

    print(
        "\nSelecting Continue with current medication → YES"
    )

    continue_yes = scroll_until_visible(
        driver,
        config.LOCATORS["continue_medication_yes"],
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    continue_yes.click()

    print(
        "Continue with current medication → YES selected."
    )

    time.sleep(0.5)

    hide_keyboard_safely(driver)

    # ========================================================
    # 3. Medication Taken From? → GOVT
    # ========================================================

    print(
        "\nSelecting Medication Taken From → GOVT"
    )

    govt_option = scroll_until_visible(
        driver,
        config.LOCATORS["medication_govt"],
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    govt_option.click()

    print(
        "Medication Taken From → GOVT selected."
    )

    time.sleep(0.5)

    hide_keyboard_safely(driver)

    print(
        "\n========== MEDICATION COMPLETE ==========\n"
    )

    return True

def select_all_lifestyle_checkboxes(driver):

    print(
        "\n========== LIFESTYLE MODIFICATION =========="
    )

    scroll_until_visible(
        driver,
        (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Advise on lifestyle modification")',
        ),
        max_scrolls=10,
        wait_after_scroll=0.15,
    )

    required_texts = {
        "Avoid alcohol and stop using tobacco products",
        "Dietary modifications (Reduce sugar content, less rice with more curry, prefer millets, increase fibre foods, avoid binge meals)",
        "Dietary modifications (salt not more than 6gms a day, oil not more than 500ml a month,avoid extra salt encourage vegitable and fruits, reduce nonvegetarian and bakery items)",
        "Physical exercise (Minimum 150mins a week)",
    }

    selected_texts = set()

    for scroll_number in range(10):

        checkboxes = driver.find_elements(
            AppiumBy.CLASS_NAME,
            "android.widget.CheckBox",
        )

        for checkbox in checkboxes:

            try:
                text = checkbox.get_attribute("text").strip()

                if text not in required_texts:
                    continue

                checked = checkbox.get_attribute("checked")

                if checked != "true":

                    checkbox.click()

                    print(
                        f"Selected: {text}"
                    )

                selected_texts.add(text)

            except Exception:
                continue

        # ----------------------------------------------------
        # IMPORTANT:
        # Stop immediately when all required options exist
        # ----------------------------------------------------

        if selected_texts >= required_texts:

            print(
                "\nAll required lifestyle options found "
                "and selected."
            )

            break

        # ----------------------------------------------------
        # Scroll only when something is still missing
        # ----------------------------------------------------

        print(
            "Some lifestyle options still missing. "
            "Scrolling..."
        )

        size = driver.get_window_size()

        driver.swipe(
            size["width"] // 2,
            int(size["height"] * 0.75),
            size["width"] // 2,
            int(size["height"] * 0.35),
            300,
        )

        time.sleep(0.15)

    print(
        "========== LIFESTYLE MODIFICATION COMPLETE ==========\n"
    )

    return True

def select_referral_not_refer(driver):

    print(
        "\n========== REFERRAL SYSTEM =========="
    )

    print(
        "Looking for Referral System → Not Refer..."
    )

    not_refer = scroll_until_visible(
        driver,
        config.LOCATORS["referral_not_refer"],
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    print(
        "Not Refer option found."
    )

    # Check whether it is already selected
    checked = not_refer.get_attribute("checked")

    print(
        f"Not Refer checked before click: {checked}"
    )

    if checked != "true":

        not_refer.click()

        time.sleep(0.5)

        print(
            "Not Refer selected."
        )

    else:

        print(
            "Not Refer was already selected."
        )

    # Verify
    checked_after = not_refer.get_attribute(
        "checked"
    )

    print(
        f"Not Refer checked after click: {checked_after}"
    )

    if checked_after != "true":

        raise RuntimeError(
            "Validation failed: Not Refer was not selected."
        )

    print(
        "\nSUCCESS: Referral → Not Refer"
    )

    print(
        "========== REFERRAL SYSTEM COMPLETE ==========\n"
    )

    return True

def inspect_camera_screen(driver):

    print("\n========== CAMERA INSPECTION ==========")

    # Inspect all clickable elements currently visible
    elements = driver.find_elements(
        AppiumBy.XPATH,
        "//*[@clickable='true']",
    )

    print(
        f"Clickable elements found: {len(elements)}"
    )

    for index, element in enumerate(elements):

        try:
            print(f"\nClickable #{index}")

            print(
                "class:",
                element.get_attribute("className"),
            )

            print(
                "resource-id:",
                element.get_attribute("resourceId"),
            )

            print(
                "text:",
                element.get_attribute("text"),
            )

            print(
                "content-desc:",
                element.get_attribute("contentDescription"),
            )

            print(
                "bounds:",
                element.get_attribute("bounds"),
            )

            print(
                "displayed:",
                element.is_displayed(),
            )

        except Exception as error:

            print(
                f"Could not inspect element: {error}"
            )

    print(
        "\n========== END CAMERA INSPECTION ==========\n"
    )


def capture_image_and_submit(driver):

    print("\n========== IMAGE CAPTURE ==========")

    # ========================================================
    # 1. FIND IMAGE CAPTURE
    # ========================================================

    print("Looking for Image Capture...")

    image_capture = scroll_until_visible(
        driver,
        config.LOCATORS["image_capture"],
        max_scrolls=15,
        wait_after_scroll=1.0,
    )

    print("Image Capture section found.")

    # ========================================================
    # 2. OPEN CAMERA
    # ========================================================

    image_capture.click()

    print("Camera icon clicked.")

    # ========================================================
    # 3. TAKE PHOTO
    # ========================================================

    print("Waiting for camera shutter...")

    shutter = WebDriverWait(
        driver,
        30,
    ).until(
        EC.element_to_be_clickable(
            config.LOCATORS["camera_shutter"]
        )
    )

    print("Take photo button found.")

    shutter.click()

    print("Photo captured.")

    time.sleep(1)

    # ========================================================
    # 4. CONFIRM PHOTO — WHITE ✓ / DONE
    # ========================================================

    print(
        "Waiting for white ✓ confirmation button..."
    )

    camera_tick = WebDriverWait(
        driver,
        30,
    ).until(
        EC.element_to_be_clickable(
            config.LOCATORS["camera_tick"]
        )
    )

    print(
        "White ✓ confirmation button found."
    )

    camera_tick.click()

    print(
        "Photo confirmed."
    )

    # ========================================================
    # 5. WAIT FOR CAMERA TO CLOSE
    # ========================================================

    print(
        "Waiting for camera to close..."
    )

    WebDriverWait(
        driver,
        30,
    ).until(
        lambda d: not d.find_elements(
            AppiumBy.ACCESSIBILITY_ID,
            "Done",
        )
    )

    print(
        "Camera closed."
    )

    # Give the MO Health form time to process
    # the returned image.
    time.sleep(1)

    # ========================================================
    # 6. WAIT FOR SUBMIT BUTTON
    # ========================================================

    print(
        "Waiting for image upload/form to return..."
    )

    submit = WebDriverWait(
        driver,
        30,
    ).until(
        EC.element_to_be_clickable(
            config.LOCATORS["submit"]
        )
    )

    print(
        "Submit button found."
    )

    # ========================================================
    # 7. SUBMIT FORM
    # ========================================================

    submit.click()

    print(
        "Submit clicked."
    )

    # ========================================================
    # 8. WAIT FOR SUCCESS
    # ========================================================

    return False


def has_follow_up_forms(driver):
    """
    Check whether at least one Follow Up form is currently available.
    """

    try:
        elements = driver.find_elements(
            AppiumBy.ID,
            "com.entrolabs.moaphealth:id/TvView",
        )

        visible = [
            element
            for element in elements
            if element.is_displayed()
        ]

        print(
            f"Follow Up forms currently visible: {len(visible)}"
        )

        return len(visible) > 0

    except Exception as error:
        print(f"Could not check Follow Up forms: {error}")
        return False


def return_to_follow_up(driver, timeout=15):
    """
    Return to the Follow Up list after completing a form.
    """

    print("\nReturning to Follow Up...")

    # First check whether we're already on the list.
    try:
        WebDriverWait(
            driver,
            2,
            poll_frequency=0.2,
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.ID,
                    "com.entrolabs.moaphealth:id/rvncdcdthree_anm",
                )
            )
        )

        print("Already on Follow Up list.")
        return True

    except Exception:
        pass

    # Otherwise navigate back.
    for attempt in range(3):

        print(
            f"Back attempt {attempt + 1}/3..."
        )

        driver.back()

        try:
            WebDriverWait(
                driver,
                timeout,
                poll_frequency=0.2,
            ).until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.ID,
                        "com.entrolabs.moaphealth:id/rvncdcdthree_anm",
                    )
                )
            )

            print(
                "Follow Up list restored."
            )

            return True

        except Exception:
            continue

    raise RuntimeError(
        "Unable to return to Follow Up list."
    )


def wait_for_follow_up_list(driver, timeout=15):
    """
    Wait until the Follow Up RecyclerView is available.
    """

    return WebDriverWait(
        driver,
        timeout,
        poll_frequency=0.2,
    ).until(
        EC.presence_of_element_located(
            (
                AppiumBy.ID,
                "com.entrolabs.moaphealth:id/rvncdcdthree_anm",
            )
        )
    )


def open_first_follow_up_patient_fast(
    driver,
    previous_patient_name=None,
):
    """
    Open the first available Follow Up form.

    If previous_patient_name is supplied, skip that patient
    when the same record is still visible after returning
    to the Follow Up records page.
    """

    wait_for_follow_up_list(driver)

    print(
        "\nLooking for available Follow Up records..."
    )

    # --------------------------------------------------------
    # Get all currently visible View buttons
    # --------------------------------------------------------

    view_buttons = driver.find_elements(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvView",
    )

    visible_views = [
        element
        for element in view_buttons
        if element.is_displayed()
    ]

    print(
        f"Visible Follow Up records: "
        f"{len(visible_views)}"
    )

    if not visible_views:

        raise RuntimeError(
            "No visible Follow Up records found."
        )

    # --------------------------------------------------------
    # Get patient names
    # --------------------------------------------------------

    patient_names = driver.find_elements(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvName",
    )

    visible_names = [
        element
        for element in patient_names
        if element.is_displayed()
    ]

    # --------------------------------------------------------
    # Find first record that is NOT the previous patient
    # --------------------------------------------------------

    selected_index = None
    patient_name = None

    for index, view_button in enumerate(
        visible_views
    ):

        try:

            if index < len(visible_names):

                current_name = (
                    visible_names[index]
                    .text
                    .strip()
                )

            else:

                current_name = "Unknown"

            print(
                f"Record #{index}: "
                f"{current_name}"
            )

            # ------------------------------------------------
            # Skip the previous record
            # ------------------------------------------------

            if (
                previous_patient_name
                and current_name.casefold()
                == previous_patient_name.casefold()
            ):

                print(
                    f"Skipping previous patient: "
                    f"{current_name}"
                )

                continue

            selected_index = index
            patient_name = current_name

            break

        except Exception as error:

            print(
                f"Could not inspect record #{index}: "
                f"{error}"
            )

            continue

    # --------------------------------------------------------
    # No new patient found
    # --------------------------------------------------------

    if selected_index is None:

        raise RuntimeError(
            "No new Follow Up record found. "
            "The previous patient may still be the "
            "only visible record."
        )

    # --------------------------------------------------------
    # Re-find View buttons immediately before clicking
    # --------------------------------------------------------

    view_buttons = driver.find_elements(
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvView",
    )

    visible_views = [
        element
        for element in view_buttons
        if element.is_displayed()
    ]

    if selected_index >= len(visible_views):

        raise RuntimeError(
            "Selected Follow Up record is no longer visible."
        )

    view_button = visible_views[
        selected_index
    ]

    print(
        f"\nOpening next available form: "
        f"{patient_name}"
    )

    view_button.click()

    return patient_name


def complete_one_form(driver):
    """
    Run the existing form workflow once.

    Use this only with your test/staging records.
    """

    print(
        "\n========== COMPLETING CURRENT FORM =========="
    )

    # --------------------------------------------------------
    # 1. MEDICINE QUESTIONS
    # --------------------------------------------------------

    print(
        "\nMedicine questions..."
    )

    fill_medicine_questions(
        driver
    )

    # --------------------------------------------------------
    # 2. DETECT WORKFLOW
    # --------------------------------------------------------

    workflow = detect_form_workflow(
        driver
    )

    print(
        f"Detected workflow: {workflow}"
    )

    # --------------------------------------------------------
    # 3. VITALS
    # --------------------------------------------------------

    print(
        "\nFilling vital fields..."
    )

    generated_values = fill_vitals_by_workflow(
        driver,
        workflow,
    )

    print(
        f"Generated values: {generated_values}"
    )

    # --------------------------------------------------------
    # 4. MEDICATION
    # --------------------------------------------------------

    print(
        "\nSelecting medication options..."
    )

    select_medication_options(
        driver
    )

    # --------------------------------------------------------
    # 5. LIFESTYLE
    # --------------------------------------------------------

    print(
        "\nSelecting lifestyle options..."
    )

    select_all_lifestyle_checkboxes(
        driver
    )

    # --------------------------------------------------------
    # 6. REFERRAL
    # --------------------------------------------------------

    print(
        "\nSelecting referral..."
    )

    select_referral_not_refer(
        driver
    )

    # --------------------------------------------------------
    # 7. IMAGE + SUBMIT
    # --------------------------------------------------------

    print(
        "\nCapturing image and submitting..."
    )

    submitted = capture_image_and_submit(
        driver
    )

    if not submitted:

        print(
            "\nForm submission was not confirmed."
        )

        return False

    print(
        "\nCurrent form completed successfully."
    )

    return True


def process_follow_up_queue_test(driver):

    completed = 0
    failed = 0

    print(
        "\n=========================================="
    )

    print(
        "STARTING FOLLOW UP QUEUE"
    )

    print(
        "=========================================="
    )

    # ========================================================
    # FIRST RECORD
    # ========================================================

    print(
        "\nOpening first Follow Up record..."
    )

    try:

        open_first_follow_up_patient_fast(
            driver
        )

    except Exception as error:

        print(
            "\nNo Follow Up records available."
        )

        print(
            f"Error: {error}"
        )

        return completed

    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        print(
            "\n------------------------------------------"
        )

        print(
            f"Processing record #{completed + failed + 1}"
        )

        print(
            "------------------------------------------"
        )

        # ====================================================
        # COMPLETE CURRENT FORM
        # ====================================================

        try:

            form_success = complete_one_form(
                driver
            )

        except Exception as error:

            failed += 1

            print(
                "\nERROR while processing form."
            )

            print(
                f"Error: {error}"
            )

            # ------------------------------------------------
            # Try to recover to Follow Up records
            # ------------------------------------------------

            try:

                recover_to_follow_up(
                    driver
                )

            except Exception as recovery_error:

                print(
                    "\nRecovery failed."
                )

                print(
                    f"Recovery error: "
                    f"{recovery_error}"
                )

                break

            # ------------------------------------------------
            # Try another record
            # ------------------------------------------------

            try:

                open_next_follow_up_patient(
                    driver
                )

            except Exception:

                print(
                    "\nNo more records."
                )

                break

            continue

        # ====================================================
        # FORM FUNCTION REPORTED FAILURE
        # ====================================================

        if not form_success:

            failed += 1

            print(
                "\nForm workflow reported failure."
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # Do not immediately assume the app is on
            # Follow Up records.
            #
            # Give the app up to 6 seconds to return.
            # ------------------------------------------------

            records_restored = (
                wait_for_follow_up_records_after_submit(
                    driver,
                    timeout=6,
                )
            )

            # ------------------------------------------------
            # Records page found
            # ------------------------------------------------

            if records_restored:

                print(
                    "\nRecords page detected."
                )

            # ------------------------------------------------
            # Records page NOT found
            # ------------------------------------------------

            else:

                print(
                    "\nSubmission timeout."
                )

                print(
                    "Recovering to Follow Up records..."
                )

                try:

                    recover_to_follow_up(
                        driver
                    )

                except Exception as error:

                    print(
                        "\nUnable to recover."
                    )

                    print(
                        f"Recovery error: {error}"
                    )

                    break

            # ------------------------------------------------
            # Find another record
            # ------------------------------------------------

            try:

                open_next_follow_up_patient(
                    driver
                )

            except Exception:

                print(
                    "\nNo more Follow Up records."
                )

                break

            continue

        # ====================================================
        # FORM FUNCTION REPORTED SUCCESS
        # ====================================================

        print(
            "\nForm submission workflow completed."
        )

        # ----------------------------------------------------
        # VERIFY RECORDS PAGE
        #
        # The app should automatically redirect here.
        # Maximum wait = 6 seconds.
        # ----------------------------------------------------

        records_restored = (
            wait_for_follow_up_records_after_submit(
                driver,
                timeout=6,
            )
        )

        # ====================================================
        # SUCCESSFUL SUBMISSION
        # ====================================================

        if records_restored:

            completed += 1

            print(
                "\n=========================================="
            )

            print(
                f"SUCCESS: RECORD #{completed}"
            )

            print(
                "Follow Up records page detected."
            )

            print(
                "=========================================="
            )

        # ====================================================
        # SUBMISSION DID NOT RETURN TO RECORDS
        # ====================================================

        else:

            failed += 1

            print(
                "\n=========================================="
            )

            print(
                "SUBMISSION TIMEOUT"
            )

            print(
                "Follow Up records page not detected "
                "within 6 seconds."
            )

            print(
                "=========================================="
            )

            # ------------------------------------------------
            # Recover only now
            # ------------------------------------------------

            try:

                recover_to_follow_up(
                    driver
                )

            except Exception as error:

                print(
                    "\nRecovery failed."
                )

                print(
                    f"Error: {error}"
                )

                break

        # ====================================================
        # FIND NEXT RECORD
        #
        # IMPORTANT:
        #
        # If successful, the app is already on the records
        # page. We DO NOT go back.
        #
        # open_next_follow_up_patient() searches and scrolls.
        # ====================================================

        try:

            print(
                "\nLooking for next Follow Up record..."
            )

            open_next_follow_up_patient(
                driver
            )

        except Exception as error:

            print(
                "\nNo more Follow Up records."
            )

            print(
                f"Queue finished: {error}"
            )

            break

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print(
        "\n=========================================="
    )

    print(
        "FOLLOW UP QUEUE FINISHED"
    )

    print(
        "=========================================="
    )

    print(
        f"Completed: {completed}"
    )

    print(
        f"Failed:    {failed}"
    )

    print(
        f"Total:     {completed + failed}"
    )

    print(
        "=========================================="
    )

    return completed

def recover_to_follow_up(
    driver,
    timeout=6,
):
    """
    Recover to Follow Up records only when necessary.

    If already on the records page:
        do NOTHING.

    If still on the patient form:
        Back once → Follow Up → Records.
    """

    records_id = (
        "com.entrolabs.moaphealth:id/"
        "rvncdcdthree_anm"
    )

    # ========================================================
    # STEP 1
    # CHECK WHETHER WE ARE ALREADY ON RECORDS
    # ========================================================

    try:

        records = driver.find_elements(
            AppiumBy.ID,
            records_id,
        )

        visible_records = [
            element
            for element in records
            if element.is_displayed()
        ]

        if visible_records:

            print(
                "\nAlready on Follow Up records."
            )

            return True

    except Exception:
        pass

    # ========================================================
    # STEP 2
    # NOT ON RECORDS → BACK ONCE
    # ========================================================

    print(
        "\nFollow Up records not visible."
    )

    print(
        "Going back ONE level..."
    )

    driver.back()

    # ========================================================
    # STEP 3
    # CHECK RECORDS AGAIN
    #
    # It is possible that one Back already returned us
    # directly to records.
    # ========================================================

    try:

        WebDriverWait(
            driver,
            2,
            poll_frequency=0.15,
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.ID,
                    records_id,
                )
            )
        )

        print(
            "Follow Up records restored."
        )

        return True

    except Exception:
        pass

    # ========================================================
    # STEP 4
    # ONLY NOW LOOK FOR FOLLOW UP BUTTON
    # ========================================================

    print(
        "Records not found after Back."
    )

    print(
        "Looking for Follow Up button..."
    )

    follow_up = wait_for_clickable(
        driver,
        "follow_up",
        timeout=timeout,
    )

    print(
        "Follow Up button found."
    )

    follow_up.click()

    # ========================================================
    # STEP 5
    # WAIT FOR RECORDS
    # ========================================================

    print(
        "Waiting for Follow Up records..."
    )

    wait_for_follow_up_list(
        driver,
        timeout=timeout,
    )

    print(
        "Follow Up records page restored."
    )

    return True

def open_next_follow_up_patient(
    driver,
    max_scrolls=30,
):
    """
    Find ANY next Follow Up record.

    IMPORTANT:
    Always scroll once before searching for a View.
    This prevents immediately reopening the same record.
    """

    print(
        "\n========== FINDING NEXT FOLLOW UP RECORD =========="
    )

    # ========================================================
    # STEP 1
    # ALWAYS SCROLL FIRST
    # ========================================================

    size = driver.get_window_size()

    width = size["width"]
    height = size["height"]

    print(
        "Immediately scrolling down..."
    )

    driver.swipe(
        width // 2,
        int(height * 0.80),
        width // 2,
        int(height * 0.30),
        250,
    )

    # Very small pause only for RecyclerView movement
    time.sleep(0.15)

    # ========================================================
    # STEP 2
    # SEARCH FOR ANY VIEW
    # ========================================================

    for scroll_number in range(max_scrolls):

        print(
            f"Searching for View "
            f"(attempt {scroll_number + 1})..."
        )

        view_buttons = driver.find_elements(
            AppiumBy.ID,
            "com.entrolabs.moaphealth:id/TvView",
        )

        visible_views = [
            element
            for element in view_buttons
            if element.is_displayed()
        ]

        print(
            f"Visible View buttons: "
            f"{len(visible_views)}"
        )

        # ====================================================
        # ANY VIEW IS ACCEPTABLE
        # ====================================================

        if visible_views:

            print(
                "View found."
            )

            visible_views[0].click()

            print(
                "Next Follow Up record opened."
            )

            return True

        # ====================================================
        # NO VIEW → SCROLL AGAIN
        # ====================================================

        print(
            "No View found. Scrolling again..."
        )

        driver.swipe(
            width // 2,
            int(height * 0.80),
            width // 2,
            int(height * 0.30),
            250,
        )

        time.sleep(0.15)

    raise RuntimeError(
        "No Follow Up View found after "
        f"{max_scrolls} scrolls."
    )

def wait_for_follow_up_records_after_submit(
    driver,
    timeout=6,
):
    """
    After Submit, wait for the Follow Up records page.

    This is the ONLY submission-result wait.
    """

    records_id = (
        "com.entrolabs.moaphealth:id/"
        "rvncdcdthree_anm"
    )

    print(
        "\nChecking for Follow Up records..."
    )

    try:

        WebDriverWait(
            driver,
            timeout,
            poll_frequency=0.15,
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.ID,
                    records_id,
                )
            )
        )

        print(
            "Follow Up records detected."
        )

        return True

    except Exception:

        print(
            f"Follow Up records not detected "
            f"within {timeout}s."
        )

        return False
import os

from dotenv import load_dotenv
from appium.webdriver.common.appiumby import AppiumBy


load_dotenv()


# ============================================================
# USER CONFIGURATION
# ============================================================

MO_USERNAME = os.getenv(
    "MO_USERNAME",
    "61757315008251",
)

MO_PASSWORD = os.getenv(
    "MO_PASSWORD",
    "Health@123",
)

VHC_NAME = os.getenv(
    "VHC_NAME",
    "Tiruchanur 1[11090232]",
)

EXCEL_PATH = os.getenv(
    "EXCEL_PATH",
    r"C:\Users\aremt\MO_Health\patients.xlsx",
)


# ============================================================
# APPIUM
# ============================================================

APPIUM_SERVER = os.getenv(
    "APPIUM_SERVER",
    "http://127.0.0.1:4723",
)

DEVICE_NAME = os.getenv(
    "DEVICE_NAME",
    "47041VDJH00065",
)

UDID = os.getenv(
    "UDID",
    "47041VDJH00065",
)


# ============================================================
# MO HEALTH APP
# ============================================================

APP_PACKAGE = os.getenv(
    "APP_PACKAGE",
    "com.entrolabs.moaphealth",
)

APP_ACTIVITY = os.getenv(
    "APP_ACTIVITY",
    "com.entrolabs.moaphealth.LoginActivity",
)


# ============================================================
# EXCEL COLUMNS
# ============================================================

COL_NAME = "Patient Name"

COL_RBS = "RBS"

COL_BP_SYSTOLIC = "BP Systolic"

COL_BP_DIASTOLIC = "BP Diastolic"

COL_PULSE = "Pulse"

COL_STATUS = "Status"


# ============================================================
# FIXED FORM VALUES
# ============================================================

MEDICINE_TAKEN_DAILY = "Yes"

TODAYS_MEDICATION = "Yes"

PREVIOUS_MEDICATION = "CHO"

CONTINUE_MEDICATION = "Yes"

MEDICATION_SOURCE = "Govt"

REFERRAL = "Not Refer"


# ============================================================
# STATUS VALUES
# ============================================================

STATUS_SUBMITTED = "Submitted"

STATUS_FAILED = "Failed"


# ============================================================
# TIMINGS
# ============================================================

WAIT_TIMEOUT = 30

LONG_WAIT_TIMEOUT = 60

MAX_ROW_RETRIES = 3

MAX_SESSION_RETRIES = 3

RETRY_BACKOFF_SECONDS = 5

SEARCH_RESULT_WAIT = 2


# ============================================================
# UI LOCATORS
# ============================================================

LOCATORS = {

    # ========================================================
    # LOGIN
    # ========================================================

    "login_username": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/EtUserName",
    ),

    "login_password": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/EtPassword",
    ),

    "login_button": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvSignin",
    ),


    # ========================================================
    # VHC
    # ========================================================

    "vhc_dropdown": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/tvSelectSecretariat",
    ),

    "vhc_search": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/EtSearch",
    ),

    "vhc_list": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/Rv_Selection",
    ),

    "vhc_item": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/CardSelection",
    ),

    "vhc_name": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/Tvname",
    ),

    "vhc_ok": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvOk",
    ),


    # ========================================================
    # NCD-CD
    # ========================================================

    "ncd_cd": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("NCD-CD")',
    ),

    "follow_up": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Follow Up")',
    ),


    # ========================================================
    # FOLLOW-UP / PATIENT SEARCH
    #
    # IMPORTANT:
    # This is NOT EtSearch.
    #
    # Runtime inspection confirmed:
    #
    # resource-id:
    # com.entrolabs.moaphealth:id/searchView
    #
    # hint:
    # Search with Name/Mobile/Health ID/UID
    # ========================================================

    "follow_up_list": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/rvncdcdthree_anm",
    ),

    "patient_name": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvName",
    ),

    "view_button": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/TvView",
    ),


    # ========================================================
    # SCREEN 1 - MEDICINE QUESTIONS
    # ========================================================

    # --------------------------------------------------------
    # Question 1
    # Whether medicine taken daily
    # --------------------------------------------------------

    "medicine_daily_yes": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/RBMedTakenYes",
    ),

    "medicine_daily_no": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/RBMedTakenNo",
    ),


    # --------------------------------------------------------
    # Question 2
    # Did the individual take today's medication
    # before coming here?
    # --------------------------------------------------------

    "before_coming_yes": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/RBindividualYes",
    ),

    "before_coming_no": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/RBindividualNo",
    ),


    # --------------------------------------------------------
    # Whether diabetic or hypertension
    # --------------------------------------------------------

    "hypor_dia_no": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/RBHyporDiaNo",
    ),
    

    # --------------------------------------------------------
    # Blood Glucose / RBS
    # --------------------------------------------------------

    "rbs_field": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/etRbsreadingnew",
    ),


    # ========================================================
    # SCREEN 2
    # ========================================================

    "bp_systolic": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/etSystole",
    ),

    "bp_diastolic": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/etDiastole",
    ),

    "pulse": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/etpulserate",
    ),


    # ========================================================
    # SCREEN 3
    # ========================================================

    "previous_medication": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Previous Medication")',
    ),

    "cho_option": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("CHO")',
    ),

    "continue_medication_yes": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Yes")',
    ),

    "medication_govt": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Govt")',
    ),


    # ========================================================
    # SCREEN 4
    # ========================================================

    "lifestyle_checkboxes": (
        AppiumBy.CLASS_NAME,
        "android.widget.CheckBox",
    ),

    "referral_not_refer": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Not Refer")',
    ),


    # ========================================================
    # IMAGE
    # ========================================================

    "image_capture": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/LLImg",
    ),

    "camera_shutter": (
        AppiumBy.ACCESSIBILITY_ID,
        "Take photo",
    ),

    "camera_tick": (
        AppiumBy.ACCESSIBILITY_ID,
        "Done",
    ),


    # ========================================================
    # SUBMIT
    # ========================================================

    "submit": (
        AppiumBy.ID,
        "com.entrolabs.moaphealth:id/tvSubmit",
    ),

    "success": (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Success")',
    ),
}
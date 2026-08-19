# MO Health Follow-up Automation

A simple, resumable Appium automation that submits NCD/CD follow-up records
into the MO Health Android app, one row at a time, from an Excel file.

## Files

| File               | Responsibility                                              |
|--------------------|---------------------------------------------------------------|
| `config.py`        | All settings: capabilities, credentials, Excel columns, locators, timeouts |
| `excel_reader.py`  | Read pending patients, mark a row Submitted / Failed         |
| `appium_driver.py` | Start/reconnect the Appium session, explicit-wait helpers     |
| `automation.py`    | One function per app screen + the resumable main loop        |
| `main.py`          | Entry point (`python main.py`)                                |

This is intentionally the *only* place logic lives — no extra layers.

## 1. Install requirements

```bash
pip install -r requirements.txt
```

You also need, separately (not pip packages):
- **Appium Server** running (`appium` on the command line, or Appium Desktop).
- **Android SDK / adb** installed and a device connected (`adb devices` should
  show it) or an emulator running.
- **UiAutomator2 driver** for Appium: `appium driver install uiautomator2`

## 2. Fill in `config.py`

This is the only file you should need to edit to point the automation at the
real app. You need to give me / fill in:

1. **Package name & launch activity** — with the app open on the phone:
   ```bash
   adb shell dumpsys window | grep -E 'mCurrentFocus'
   ```
   This prints something like `com.mohealth.app/.MainActivity`. Put those into
   `CAPABILITIES["appPackage"]` and `CAPABILITIES["appActivity"]`.

2. **Device name** — output of `adb devices`.

3. **Login credentials** — `LOGIN_USERNAME` / `LOGIN_PASSWORD`.

4. **Locators** — this is the biggest piece. Every screen (login, menu, search,
   follow-up form, image picker, submit) needs its real element IDs. Get them with:
   - **Appium Inspector** (recommended) — connect it to the same Appium server
     and device, open each screen, click each field/button, and copy its
     `resource-id`.
   - Or `adb shell uiautomator dump` + `uiautomatorviewer` if you prefer.

   Every locator lives in the `LOCATORS` dictionary in `config.py`, keyed by a
   descriptive name (e.g. `"login_username_field"`). Replace the placeholder
   `(AppiumBy.ID, "com.mohealth.app:id/...")` values with the real ones. Nothing
   in `automation.py` needs to change — it only ever refers to locators by key.

   **Send me screenshots of these screens and I'll fill in the exact locators
   with you:** Login screen, main menu / navigation drawer, NCD/CD Follow-ups
   list + search, an opened patient's follow-up form (all fields), the
   "attach image" button + whatever picker/chooser appears after tapping it,
   and the submit/success screen.

## 3. Prepare the Excel file

Default path: `patients.xlsx` (change `EXCEL_PATH` in `config.py` if needed).
Required header row (exact column names, case-sensitive, order doesn't matter):

| Patient Name | BP | Sugar | Height | Weight | BMI | Medicine | Symptoms | Doctor Notes | Visit Date | Image Path | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|

- `Image Path` — a path on **the machine running this script** (not the phone);
  the script pushes it to the device automatically.
- `Status` — leave blank for rows not yet processed. The script writes
  `Submitted` on success or `Failed: <reason>` on failure.

**Send me a sample Excel file** (even with 2-3 dummy rows) and I'll verify
`excel_reader.py` reads it correctly before we run anything against the real
app.

## 4. Run it

```bash
# in one terminal
appium

# in another terminal
python main.py
```

Expected terminal output:

```
Reading Excel...
Logging in...
Navigating to Follow-ups...
Searching: John Kumar
Opening Record...
Uploading Image...
Submitting...
Success
Next Record...
...
All patients processed. Done.
```

## How resuming / error recovery works

- **Progress is saved after every single patient**, immediately, directly into
  the Excel file (`Status` = `Submitted`). If the script is killed at any
  point, nothing already-submitted is lost.
- On every run, `excel_reader.get_pending_patients()` re-reads the file and
  returns only rows that are **not** `Submitted` and **not** already `Failed`
  — so restarting the script always continues from the correct next patient,
  never from row 1.
- If Appium/the device/the app misbehaves mid-patient (session dies, app
  crashes, phone disconnects), the same row is retried (session is
  reconnected, app relaunched, login redone) up to `MAX_SESSION_RETRIES` /
  `MAX_ROW_RETRIES` times (see `config.py`) **before** moving on — the current
  patient is never skipped just because of a connection blip.
- If a row genuinely fails (patient not found, app rejects the submission,
  etc.) after `MAX_ROW_RETRIES` attempts, it's written as
  `Failed: <reason>` and the script moves to the next patient rather than
  getting stuck.
- To retry a row marked `Failed`, just clear its `Status` cell (or set it to
  `Pending`) and run `python main.py` again.

## Suggested build order (test each stage before the next)

1. **Excel only** — run just `excel_reader.load_patients()` /
   `get_pending_patients()` against your real sample file and print the
   result, with no Appium involved yet.
2. **Session + login** — get `appium_driver.create_session()` and
   `automation.login()` working against the real app.
3. **Navigation + search** — one patient, get to the follow-up form.
4. **Form fill + image upload** — the fiddliest part; the image picker flow
   in `automation.upload_image()` is the most app-specific piece and will
   likely need adjusting once we see the real chooser dialog.
5. **Submit + success detection.**
6. **Full loop** across the whole Excel file, then deliberately kill the
   script mid-run (e.g. `Ctrl+C` after 2 patients) and re-run it to confirm
   it resumes instead of restarting.
7. **Error injection** — turn off Wi-Fi/airplane mode mid-run, or force-stop
   the app from `adb`, to confirm reconnect + resume behaves as expected.

## What I still need from you to finish wiring this up

- [ ] Real `appPackage` / `appActivity`
- [ ] Real device name (`adb devices` output)
- [ ] Screenshots (or an Appium Inspector session) of: login screen, main
      menu, follow-ups search screen, follow-up form, image attach/picker
      flow, submit/success screen
- [ ] A sample `patients.xlsx` (even with fake data) to confirm columns line up
- [ ] Confirmation of how "attach image" behaves — does it open the system
      Gallery, a Files app, or the app's own built-in picker?

# Alisa Trial Abuser

[Русская версия](README.ru.md)

This app opens a registration page, fills in the required details, selects
Windows, and shows the received VPN link.

It can be used in two ways:

- GUI app: run `alisa-trial-abuser.exe`
- CLI script: run `register_vpn_link.py` from the terminal

## Important

This app is provided for educational purposes and must be used only on websites,
systems, and accounts where you have permission to automate the flow. Do not use
it to bypass limits, violate service rules, or access anything without
permission.

## GUI Usage

Unzip the app archive and open:

```text
alisa-trial-abuser.exe
```

The app first tries to use Microsoft Edge. If Edge is not available, it tries
Google Chrome. If neither browser is available, the app can download Playwright
Chromium on this computer.

In the app window:

1. Check the fields in the `Settings` section.
2. Enable `Show browser window` if you want to see the browser.
3. Click `Start`.
4. Wait for the result.
5. Click `Copy link` to copy the link.

## CLI Usage

Install dependencies first:

```powershell
pip install playwright
python -m playwright install chromium
```

Run with default settings:

```powershell
python .\register_vpn_link.py
```

Show the browser window:

```powershell
python .\register_vpn_link.py --headful
```

Override values for one run:

```powershell
python .\register_vpn_link.py --password "AnotherPassword123"
```

```powershell
python .\register_vpn_link.py --email-domain "mail.com"
```

Example output:

```text
Generated email: qwerty_ab12cd34@mail.ru
https://sub.example.com/example_link
```

## CLI Parameters

All parameters are optional.

| Parameter | Meaning |
| --- | --- |
| `--url` | Registration page URL |
| `--password` | Password entered into the form |
| `--email-prefix` | Prefix used for the generated email |
| `--email-domain` | Domain used for the generated email |
| `--device-text` | Text used to select the Windows option |
| `--browser-channel` | Browser mode: `auto`, `msedge`, `chrome`, or `chromium` |
| `--no-download-chromium` | Disables Chromium download fallback |
| `--headful` | Shows the browser window |
| `--timeout-ms` | Maximum wait time for page actions |
| `--email-selector` | Selector for the email field |
| `--password-selector` | Selector for the password field |
| `--submit-selector` | Selector for the submit button |
| `--link-selector` | Optional selector for the link field |
| `--copied-selector` | Optional selector for an extra button after the link step |

## Window Fields

`URL` - registration page address.

`Password` - password entered into the form.

`Email prefix` - beginning of the generated email address.

`Email domain` - domain of the generated email address.

`Device text` - text used to select the Windows option.

`Browser` - browser used by the app. `auto` tries Edge first, then Chrome.

`Show browser window` - shows the browser while the app is running.

`Download Chromium if needed` - downloads Playwright Chromium if Edge and Chrome
are not available. Internet connection is required for this download.

`Timeout ms` - maximum wait time for page actions.

`Link selector` - can be left empty. Use it only when the link must be read from
a specific page field.

## Result

After a successful run, the app shows or prints:

`Generated email` - the email address used by the app.

`Link` - the VPN link found by the app.

## If Something Goes Wrong

Enable `Show browser window` and run again. This helps you see where the flow
stops.

If the app cannot find the expected screen or link, it may create a screenshot:

```text
no_windows_card_found.png
no_vpn_link_found.png
```

Use the screenshot to check what was visible in the browser when the error
happened.


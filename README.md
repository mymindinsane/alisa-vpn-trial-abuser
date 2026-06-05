# Register VPN Link Script

Python script that opens a registration page in Chromium, fills an email and
password, selects the Windows device option, then prints the received VPN link
to the console.

## Notice

This project is provided for educational purposes and for use only on websites,
systems, and accounts where you have explicit permission to automate the flow.
Do not use it to bypass service limits, violate terms of service, create
unauthorized accounts, or access systems without permission.

The script has hardcoded defaults at the top of `register_vpn_link.py`. Command
line parameters are optional and only override those defaults for the current
run.

## What It Does

1. Opens the registration page.
2. Generates an email in the format `qwerty_XXXXXXXX@mail.ru`.
3. Enters the generated email and password.
4. Submits the form.
5. Selects the Windows option on the device screen.
6. Searches the next page for a VPN/config link.
7. Prints the generated email and link in the terminal.

## Requirements

- Python 3.9 or newer
- Playwright for Python
- Chromium installed through Playwright

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Playwright:

```powershell
pip install playwright
```

Install Chromium:

```powershell
python -m playwright install chromium
```

## Run With Defaults

```powershell
python .\register_vpn_link.py
```

Example console output:

```text
Generated email: qwerty_ab12cd34@mail.ru
https://sub.alisavpn.ru/example_link
```

## How To Work With It

### 1. First Run

Start with the default command:

```powershell
python .\register_vpn_link.py
```

If everything works, the terminal prints two lines:

```text
Generated email: qwerty_ab12cd34@mail.ru
https://sub.alisavpn.ru/example_link
```

The first line is the email generated for this run. The second line is the link
found on the result page.

### 2. Show The Browser

Use `--headful` when you want to see what the browser is doing:

```powershell
python .\register_vpn_link.py --headful
```

This is useful when the script stops, clicks the wrong element, or does not find
the link.

To make visible browser mode permanent, edit the default in
`register_vpn_link.py`:

```python
HEADFUL = True
```

### 3. Change Values For One Run

Pass parameters in the terminal when you want to change something only once:

```powershell
python .\register_vpn_link.py --email-domain "mail.com"
```

```powershell
python .\register_vpn_link.py --password "AnotherPassword123"
```

### 4. Change Defaults Permanently

Edit constants at the top of `register_vpn_link.py` when you want the script to
use new values every time:

```python
PASSWORD = "AnotherPassword123"
EMAIL_DOMAIN = "mail.com"
HEADFUL = True
```

Command line parameters still have priority over these defaults.

### 5. Fix Selectors If The Page Changes

Playwright finds elements through selectors:

```python
EMAIL_SELECTOR = "input[type='email']"
PASSWORD_SELECTOR = "input[type='password']"
SUBMIT_SELECTOR = "button[type='submit']"
```

If the page changes and the script cannot fill or click something, run with
`--headful` first. Then inspect the page in the browser and update the selector
or pass it through the terminal:

```powershell
python .\register_vpn_link.py --email-selector "input[name='email']"
```

### 6. Fix Link Detection

By default, the script scans common elements and page text. If the link is always
inside one known field, provide it directly:

```powershell
python .\register_vpn_link.py --link-selector "input"
```

Or set the default in `register_vpn_link.py`:

```python
LINK_SELECTOR = "input"
```

### 7. Read Error Screenshots

When the script cannot continue, it saves a screenshot in the current folder:

- `no_windows_card_found.png` means the Windows card was not found.
- `no_vpn_link_found.png` means the link was not found.

Open the screenshot, check what page is visible, then adjust the matching
selector or text.

## Override Defaults

You can pass only the values you want to change. Everything else still comes
from the hardcoded defaults.

Show the browser window:

```powershell
python .\register_vpn_link.py --headful
```

Use another password:

```powershell
python .\register_vpn_link.py --password "AnotherPassword123"
```

Use another email domain:

```powershell
python .\register_vpn_link.py --email-domain "mail.com"
```

Override several values:

```powershell
python .\register_vpn_link.py `
  --email-prefix "qwerty" `
  --email-domain "mail.com" `
  --device-text "Windows" `
  --timeout-ms 45000
```

## Hardcoded Defaults

The main defaults are at the top of `register_vpn_link.py`:

```python
REGISTER_URL = "https://alisavpn.cc/auth/register"
PASSWORD = "Qwerty12345!"
EMAIL_PREFIX = "qwerty"
EMAIL_DOMAIN = "mail.ru"
DEVICE_TEXT = "Windows"
HEADFUL = False
TIMEOUT_MS = 30000
```

## Command Line Parameters

Every parameter is optional.

| Parameter | Uses default from | Meaning |
| --- | --- | --- |
| `--url` | `REGISTER_URL` | Registration page URL |
| `--password` | `PASSWORD` | Password entered into the form |
| `--email-prefix` | `EMAIL_PREFIX` | Email prefix before the random suffix |
| `--email-domain` | `EMAIL_DOMAIN` | Email domain after `@` |
| `--device-text` | `DEVICE_TEXT` | Text used to find the Windows card |
| `--headful` | `HEADFUL` | Opens a visible browser window |
| `--timeout-ms` | `TIMEOUT_MS` | Timeout for actions and waits |
| `--email-selector` | `EMAIL_SELECTOR` | Selector for the email field |
| `--password-selector` | `PASSWORD_SELECTOR` | Selector for the password field |
| `--submit-selector` | `SUBMIT_SELECTOR` | Selector for the submit button |
| `--link-selector` | `LINK_SELECTOR` | Optional selector for the link element |
| `--copied-selector` | `COPIED_SELECTOR` | Optional selector for an extra button after the link step |

## Selectors

If the page markup changes, update these constants or pass their command line
equivalents:

```python
EMAIL_SELECTOR = "input[type='email']"
PASSWORD_SELECTOR = "input[type='password']"
SUBMIT_SELECTOR = "button[type='submit']"
LINK_SELECTOR = None
COPIED_SELECTOR = None
```

Example:

```powershell
python .\register_vpn_link.py `
  --email-selector "input[name='email']" `
  --password-selector "input[name='password']" `
  --submit-selector "button[type='submit']" `
  --link-selector "input"
```

## Link Search

By default, the script searches for a link in:

- `input`
- `textarea`
- `code`
- `pre`
- `a`
- page text

If the link is always inside a known element, pass `--link-selector` or set
`LINK_SELECTOR` in the script.

## Troubleshooting

If the Windows card is not found, the script saves a screenshot named
`no_windows_card_found.png`.

If the link is not found, the script saves a screenshot named
`no_vpn_link_found.png`.

Use `--headful` to watch the browser and see where the flow stops.

## License

A common GitHub choice for a small script like this is the MIT License because
it is simple and widely understood.

Important: a license does not make improper use legal. It only describes how
others may copy, modify, and distribute the code. Keep the notice above in the
README, and consider adding the same idea to the repository description.

Suggested repository wording:

```text
Educational Playwright automation example. Use only on systems you own or have
permission to automate.
```

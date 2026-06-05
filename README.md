# Alisa Trial Abuse Tester

Command-line version of Alisa Trial Abuse Tester.

It opens a registration page in Chromium, fills in an email and password,
selects the Windows option, and prints the received VPN link in the terminal.

## Important

This project is provided for educational purposes and must be used only on
websites, systems, and accounts where you have permission to automate the flow.
Do not use it to bypass service limits, violate service rules, create
unauthorized accounts, or access anything without permission.

## Requirements

- Python 3.9 or newer
- Playwright for Python
- Playwright Chromium

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install playwright
python -m playwright install chromium
```

## Run

Start with the default settings:

```powershell
python .\register_vpn_link.py
```

Example output:

```text
Generated email: qwerty_ab12cd34@mail.ru
https://sub.example.com/example_link
```

The first line is the generated email. The second line is the received link.

## Show The Browser

Use `--headful` to see the browser window while the script is running:

```powershell
python .\register_vpn_link.py --headful
```

This is useful when you want to see where the flow stops.

## Override Settings

The script has default values inside `register_vpn_link.py`, but you can
override them for one run.

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

## Parameters

All parameters are optional.

| Parameter | Meaning |
| --- | --- |
| `--url` | Registration page URL |
| `--password` | Password entered into the form |
| `--email-prefix` | Prefix used for the generated email |
| `--email-domain` | Domain used for the generated email |
| `--device-text` | Text used to select the Windows option |
| `--headful` | Shows the browser window |
| `--timeout-ms` | Maximum wait time for page actions |
| `--email-selector` | Selector for the email field |
| `--password-selector` | Selector for the password field |
| `--submit-selector` | Selector for the submit button |
| `--link-selector` | Optional selector for the link field |
| `--copied-selector` | Optional selector for an extra button after the link step |

## Link Search

If `--link-selector` is not set, the script searches for a link in:

- `input`
- `textarea`
- `code`
- `pre`
- `a`
- visible page text

If the link is always inside a known element, pass the selector:

```powershell
python .\register_vpn_link.py --link-selector "input"
```

## Troubleshooting

If the Windows option is not found, the script saves:

```text
no_windows_card_found.png
```

If the link is not found, the script saves:

```text
no_vpn_link_found.png
```

Open the screenshot to see what was displayed in the browser when the error
happened.

## License

MIT License is a common choice for a small script like this.

Important: a license does not make improper use legal. It only describes how
others may copy, modify, and distribute the code.

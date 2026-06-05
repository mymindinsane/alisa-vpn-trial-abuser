# VPN Link App

This app opens a registration page, fills in the required details, selects
Windows, and shows the received VPN link in the app window.

## Important

This app is provided for educational purposes and must be used only on websites,
systems, and accounts where you have permission to automate the flow. Do not use
it to bypass limits, violate service rules, or access anything without
permission.

## How To Start

Unzip the app archive and open:

```text
vpn-link-gui.exe
```

Do not delete this folder:

```text
ms-playwright
```

The app needs it to run the bundled browser.

## How To Use

1. Open `vpn-link-gui.exe`.
2. Check the fields in the `Settings` section.
3. Enable `Show browser window` if you want to see the browser.
4. Click `Start`.
5. Wait for the result.
6. Click `Copy link` to copy the link.

## Window Fields

`URL` - registration page address.

`Password` - password entered into the form.

`Email prefix` - beginning of the generated email address.

`Email domain` - domain of the generated email address.

`Device text` - text used to select the Windows option.

`Timeout ms` - maximum wait time for page actions.

`Link selector` - can be left empty. Use it only when the link must be read from
a specific page field.

## Result

After a successful run, the `Result` section shows:

`Generated email` - the email address used by the app.

`Link` - the VPN link found by the app.

The `Copy link` button copies the link to your clipboard.

## If Something Goes Wrong

Enable `Show browser window` and run the app again. This helps you see where the
flow stops.

If the app cannot find the expected screen or link, it may create a screenshot
next to the app:

```text
no_windows_card_found.png
no_vpn_link_found.png
```

Use the screenshot to check what was visible in the browser when the error
happened.


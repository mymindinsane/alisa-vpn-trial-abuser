import argparse
import os
import random
import re
import sys
import string
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


# Main settings. If the page changes, start by checking these constants.
REGISTER_URL = "https://alisavpn.cc/auth/register"
PASSWORD = "Qwerty12345!"
EMAIL_PREFIX = "qwerty"
EMAIL_DOMAIN = "mail.ru"
DEVICE_TEXT = "Windows"

# HEADFUL controls whether the browser window is visible.
# False = run in the background, True = show Chromium on screen.
HEADFUL = False

# Default timeout for Playwright actions: clicks, fills, waits, selectors.
TIMEOUT_MS = 30000

# CSS selectors for the registration form fields and submit button.
EMAIL_SELECTOR = "input[type='email']"
PASSWORD_SELECTOR = "input[type='password']"
SUBMIT_SELECTOR = "button[type='submit']"

# Optional selectors for pages with stable markup. Keep None to use fallback search.
LINK_SELECTOR = None
COPIED_SELECTOR = None

# Regex that recognizes common VPN/config links and regular HTTPS links.
VPN_LINK_RE = re.compile(r"(?:vless|vmess|trojan|ss|wireguard|wg|https?)://[^\s\"'<>]+", re.I)


def configure_packaged_browser_path() -> None:
    """Use a bundled Playwright browser folder when running as a packaged exe."""
    app_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    bundled_browsers = app_dir / "ms-playwright"

    if bundled_browsers.exists() and "PLAYWRIGHT_BROWSERS_PATH" not in os.environ:
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(bundled_browsers)


def parse_args():
    """Read optional command-line overrides, using constants above as defaults."""
    parser = argparse.ArgumentParser(description="Register and print the received VPN/config link.")
    parser.add_argument("--url", default=REGISTER_URL)
    parser.add_argument("--password", default=PASSWORD)
    parser.add_argument("--email-prefix", default=EMAIL_PREFIX)
    parser.add_argument("--email-domain", default=EMAIL_DOMAIN)
    parser.add_argument("--device-text", default=DEVICE_TEXT)
    parser.add_argument("--headful", action="store_true", default=HEADFUL)
    parser.add_argument("--timeout-ms", type=int, default=TIMEOUT_MS)
    parser.add_argument("--email-selector", default=EMAIL_SELECTOR)
    parser.add_argument("--password-selector", default=PASSWORD_SELECTOR)
    parser.add_argument("--submit-selector", default=SUBMIT_SELECTOR)
    parser.add_argument("--link-selector", default=LINK_SELECTOR)
    parser.add_argument("--copied-selector", default=COPIED_SELECTOR)
    return parser.parse_args()


def default_settings():
    """Return the same defaults as parse_args, but without reading CLI arguments."""
    return SimpleNamespace(
        url=REGISTER_URL,
        password=PASSWORD,
        email_prefix=EMAIL_PREFIX,
        email_domain=EMAIL_DOMAIN,
        device_text=DEVICE_TEXT,
        headful=HEADFUL,
        timeout_ms=TIMEOUT_MS,
        email_selector=EMAIL_SELECTOR,
        password_selector=PASSWORD_SELECTOR,
        submit_selector=SUBMIT_SELECTOR,
        link_selector=LINK_SELECTOR,
        copied_selector=COPIED_SELECTOR,
    )


def generate_email(args) -> str:
    """Build one email address from a fixed prefix and a random suffix."""
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{args.email_prefix}_{suffix}@{args.email_domain}"


def first_link_from_text(text: str) -> Optional[str]:
    """Return the first URL-like VPN/config link found in the given text."""
    match = VPN_LINK_RE.search(text)
    return match.group(0) if match else None


def click_windows_device(page, args) -> None:
    """Wait for the device screen and click the Windows option."""
    page.wait_for_load_state("networkidle")

    try:
        # get_by_text searches visible page text. exact=False allows matching
        # a larger label such as "Computer Windows" or localized variants.
        page.get_by_text(args.device_text, exact=False).first.click()
        return
    except PlaywrightTimeoutError:
        pass

    # A screenshot is useful when the page changed and the selector no longer works.
    screenshot = Path("no_windows_card_found.png").resolve()
    page.screenshot(path=str(screenshot), full_page=True)
    raise RuntimeError(f"Windows device card was not found. Screenshot saved to: {screenshot}")


def extract_link(page, args) -> Optional[str]:
    """Find a VPN/config link on the current page."""
    page.wait_for_load_state("networkidle")

    if args.link_selector:
        # If you know the exact element, this is the fastest and most stable path.
        link_element = page.locator(args.link_selector).first
        value = ""
        try:
            # input_value works for form fields, but throws for normal elements.
            value = link_element.input_value(timeout=1000)
        except PlaywrightError:
            pass
        return first_link_from_text(value) or first_link_from_text(link_element.text_content() or "")

    # Fallback: scan common places where a link can be displayed.
    for selector in ("input", "textarea", "code", "pre", "a"):
        elements = page.locator(selector)
        for index in range(elements.count()):
            element = elements.nth(index)
            text = ""
            try:
                if selector in ("input", "textarea"):
                    # Text inside input/textarea is stored as value, not text_content.
                    text = element.input_value(timeout=1000)
                else:
                    text = element.text_content(timeout=1000) or ""
            except PlaywrightTimeoutError:
                continue

            link = first_link_from_text(text)
            if link:
                return link

    # Last fallback: scan all visible body text.
    return first_link_from_text(page.locator("body").inner_text())


def run_registration_flow(args, log=print):
    """Run the browser flow once and return the generated email and found link."""
    configure_packaged_browser_path()
    email = generate_email(args)

    with sync_playwright() as p:
        # Launch Chromium and create a fresh tab/page.
        browser = p.chromium.launch(headless=not args.headful)
        page = browser.new_page()
        page.set_default_timeout(args.timeout_ms)

        try:
            log(f"Generated email: {email}")

            # Open the registration page and fill the form.
            log("Opening registration page...")
            page.goto(args.url, wait_until="domcontentloaded")
            page.locator(args.email_selector).fill(email)
            page.locator(args.password_selector).fill(args.password)
            page.locator(args.submit_selector).click()

            # Continue through the post-registration device step.
            log("Selecting Windows device...")
            click_windows_device(page, args)
            log("Searching for link...")
            link = extract_link(page, args)

            if not link:
                screenshot = Path("no_vpn_link_found.png").resolve()
                page.screenshot(path=str(screenshot), full_page=True)
                raise RuntimeError(f"VPN link was not found. Screenshot saved to: {screenshot}")

            if args.copied_selector:
                page.locator(args.copied_selector).first.click()

            return email, link
        finally:
            # Always close the browser, even if an error happened.
            browser.close()


def main() -> int:
    args = parse_args()

    try:
        _, link = run_registration_flow(args)
        print(link)
        return 0
    except (PlaywrightTimeoutError, RuntimeError) as exc:
        print(f"Failed to complete registration flow: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

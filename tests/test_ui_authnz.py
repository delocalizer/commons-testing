from random import randint
import re

import pytest

from playwright.sync_api import Page, expect

from .conftest import Settings


def test_anonymous_browsing(settings: Settings, page: Page) -> None:
    """
    An anonymous user should see certain things, not others.
    """
    page.goto(settings.BASE_URL)

    expect(page.get_by_role("button", name="Login")).to_have_count(1)

    # Dictionary table view is visible (Program is required for all Gen3 dictionaries)
    page.get_by_role("link").filter(has_text="Dictionary").click()
    expect(
        page.get_by_role("button", name="Program A broad framework of")
    ).to_be_visible()
    # Dictionary graph view is visible
    page.get_by_role("button", name="Graph View").click()
    expect(page.locator("canvas")).to_be_visible()

    # Exploration shows no records by default
    page.get_by_role("link").filter(has_text="Exploration").click()
    page.get_by_role("tab", name="Data Files").click()
    expect(page.get_by_role("table")).to_contain_text("No records to display")
    page.get_by_role("link").filter(has_text="Exploration").click()
    page.get_by_role("tab", name="Cases").click()
    expect(page.get_by_label("Cases", exact=True).locator("td")).to_contain_text(
        "No records to display"
    )

    # Workspaces is not available
    page.get_by_role("link").filter(has_text="Workspace").click()
    expect(page.get_by_role("main")).to_contain_text(
        "You are not logged in and cannot access this protected content."
    )

    # Profile is not available
    page.get_by_role("link").filter(has_text="Profile").click()
    expect(page.get_by_role("main")).to_contain_text(
        "You are not logged in and cannot access this protected content."
    )


@pytest.mark.auth0
def test_valid_login_ux(settings: Settings, page: Page) -> None:
    """
    A registered user should be able to log in
    """
    page.goto(settings.BASE_URL)
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="LOGIN", exact=True).click()
    # Auth0 lock
    expect(page.get_by_role("textbox", name="Email address")).to_be_visible()
    expect(page.get_by_role("textbox", name="Password")).to_be_visible()
    expect(page.get_by_role("link", name="Forgot password?")).to_be_visible()
    expect(page.get_by_role("link", name="Sign up")).to_be_visible()
    # Login
    page.get_by_role("textbox", name="Email address").click()
    page.get_by_role("textbox", name="Email address").fill(
        settings.USER_TIER2_USERNAME.get_secret_value()
    )
    page.get_by_role("textbox", name="Email address").press("Tab")
    page.get_by_role("textbox", name="Password").fill(
        settings.USER_TIER2_PASSWORD.get_secret_value()
    )
    page.get_by_role("button", name="Continue", exact=True).click()

    # top bar no longer shows Login button
    expect(page.get_by_role("button", name="Login")).to_have_count(0)
    expect(
        page.locator("div").filter(has_text=re.compile(r"^auth0\|[0-9a-f]+$")).first
    ).to_be_visible()


@pytest.mark.auth0
def test_invalid_login_ux(settings: Settings, page: Page) -> None:
    """
    Supplying the wrong credentials does not get you a login
    """
    page.goto(settings.BASE_URL)

    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="LOGIN", exact=True).click()
    randomusr = ''.join(chr(randint(33,125)) for i in range(20))
    randompwd = ''.join(chr(randint(33,125)) for i in range(10))
    page.get_by_role("textbox", name="Email address").fill(randomusr)
    page.get_by_role("textbox", name="Email address").press("Tab")
    page.get_by_role("textbox", name="Password").fill(randompwd)
    page.get_by_role("button", name="Continue", exact=True).click()
    expect(page.locator("#error-element-password")).to_contain_text(
        "Wrong email or password"
    )

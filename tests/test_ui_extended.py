from random import randint
import re

import pytest

from playwright.sync_api import Page, expect

from .conftest import Settings


@pytest.mark.parametrize("page_as_role", ["tier1"], indirect=True)
def test_tier1_views(settings: Settings, page_as_role: Page) -> None:
    """
    An anonymous user should see certain things, not others.
    """
    page = page_as_role
    page.goto(settings.BASE_URL)

    # Login is visible
    expect(page.get_by_role("button", name="Login")).to_have_count(1)

    # Exploration view
    page.get_by_role("link").filter(has_text="Exploration").click()
    page.get_by_role("tab", name="Data Files").click()
    page.get_by_role("link").filter(has_text="Exploration").click()
    page.get_by_role("tab", name="Cases").click()

    # Dictionary table view is visible
    page.get_by_role("link").filter(has_text="Dictionary").click()
    # (Program is required for all Gen3 dictionaries)
    expect(
        page.get_by_role("button", name="Program A broad framework of")
    ).to_be_visible()

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
def test_invalid_login_ux(settings: Settings, page: Page) -> None:
    """
    Supplying the wrong credentials does not get you a login
    """
    page.goto(settings.BASE_URL)

    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="LOGIN", exact=True).click()
    randomusr = "".join(chr(randint(33, 125)) for i in range(20))
    randompwd = "".join(chr(randint(33, 125)) for i in range(10))
    page.get_by_role("textbox", name="Email address").fill(randomusr)
    page.get_by_role("textbox", name="Password").fill(randompwd)
    page.get_by_role("button", name="Continue", exact=True).click()
    expect(page.locator("#error-element-password")).to_contain_text(
        "Wrong email or password"
    )


@pytest.mark.parametrize("page_as_role", ["tier2", "tier3"], indirect=True)
def test_valid_login_view(settings: Settings, page_as_role: Page) -> None:
    """
    A logged in user shows as logged in
    """
    page = page_as_role
    page.goto(settings.BASE_URL)
    expect(page.get_by_role("button", name="Logout")).to_be_visible()
    # top bar no longer shows Login button
    expect(page.get_by_role("button", name="Login")).to_have_count(0)

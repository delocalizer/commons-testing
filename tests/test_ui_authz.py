import pytest

from playwright.sync_api import Page, expect

from .conftest import Settings


def test_anonymous_browsing(settings: Settings, page: Page) -> None:
    """
    An anonymous user should see certain things, not others.
    """
    page.goto(settings.BASE_URL)

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

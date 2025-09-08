import pytest

from playwright.sync_api import Page, expect

from .conftest import Settings


@pytest.mark.smoke
def test_homepage(settings: Settings, page: Page) -> None:
    """
    The data commons homepage is live at the expected URL
    """
    page.goto(settings.BASE_URL)
    assert page.is_visible("body")


@pytest.mark.parametrize("page_as_role", ["tier1"], indirect=True)
def test_homepage_appearance(settings: Settings, page_as_role: Page) -> None:
    """
    The data commons homepage should always display certain elements.
    """
    page = page_as_role
    page.goto(settings.BASE_URL)

    # top bar
    expect(page.get_by_role("button", name="Browse Data")).to_be_visible()
    expect(page.get_by_role("button", name="Documentation")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    # navigation links (tabs) — these will differ according to frontend version
    # and configuration
    expect(page.get_by_role("link").filter(has_text="Dictionary")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Exploration")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Query")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Analysis")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Workspace")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Profile")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Data Library")).to_be_visible()

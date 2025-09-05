import pytest

from playwright.sync_api import Page, expect

from .conftest import Settings


@pytest.mark.smoke
def test_homepage(settings: Settings, page: Page) -> None:
    """
    The data commons homepage is live at the expected URL
    """
    page.goto(settings.BASE_URL)
    expect(page.get_by_role("link", name="link back to homepage")).to_be_visible()


def test_homepage_appearance(settings: Settings, page: Page) -> None:
    """
    The data commons homepage should display certain elements.
    """
    page.goto(settings.BASE_URL)

    # top bar
    expect(page.get_by_role("button", name="Browse Data")).to_be_visible()
    expect(page.get_by_role("button", name="Documentation")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    # navigation links (tabs)
    expect(page.get_by_role("link").filter(has_text="Dictionary")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Exploration")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Query")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Analysis")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Workspace")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Profile")).to_be_visible()
    expect(page.get_by_role("link").filter(has_text="Data Library")).to_be_visible()


@pytest.mark.datamodel
def test_data_dictionary_details(settings: Settings, page: Page) -> None:
    """
    Data model-specific expectations of the data dictionary view
    """
    page.goto(settings.BASE_URL)

    page.get_by_role("link").filter(has_text="Dictionary").click()
    expect(page.get_by_role("main")).to_contain_text(
        "The current commons dictionary has 19 nodes and 198 properties"
    )

    expect(page.get_by_role("heading", name="Administrative")).to_be_visible()
    expect(page.get_by_role("button", name="Acknowledgement")).to_be_visible()
    expect(page.get_by_role("button", name="Core Metadata Collection")).to_be_visible()
    expect(
        page.get_by_role("button", name="Program A broad framework of")
    ).to_be_visible()
    expect(
        page.get_by_role("button", name="Publication Publication for a")
    ).to_be_visible()

    expect(page.get_by_role("heading", name="Data File")).to_be_visible()
    expect(
        page.get_by_role(
            "button", name="Aligned Reads File Data file containing aligned reads"
        )
    ).to_be_visible()
    expect(page.get_by_role("button", name="Lipidomics File Data file")).to_be_visible()
    expect(
        page.get_by_role("button", name="Metabolomics File Data file")
    ).to_be_visible()
    expect(page.get_by_role("button", name="Proteomics File Data file")).to_be_visible()
    expect(page.get_by_role("button", name="Unaligned Reads File Data")).to_be_visible()

    expect(page.get_by_role("heading", name="Analysis")).to_be_visible()
    expect(
        page.get_by_role("button", name="Alignment Workflow Metadata")
    ).to_be_visible()

    expect(page.get_by_role("heading", name="Clinical")).to_be_visible()
    expect(page.get_by_role("button", name="Demographic Data for the")).to_be_visible()
    expect(page.get_by_role("button", name="Medical History Medical")).to_be_visible()
    expect(page.get_by_role("button", name="Subject An individual")).to_be_visible()

    expect(page.get_by_role("heading", name="Experimental Methods")).to_be_visible()
    expect(
        page.get_by_role("button", name="Genomics Assay Details about")
    ).to_be_visible()
    expect(page.get_by_role("button", name="Lipidomics Assay Details")).to_be_visible()
    expect(
        page.get_by_role("button", name="Metabolomics Assay Details")
    ).to_be_visible()
    expect(page.get_by_role("button", name="Proteomics Assay Details")).to_be_visible()

    expect(page.get_by_role("heading", name="Biospecimen")).to_be_visible()
    expect(page.get_by_role("button", name="Sample Biospecimen")).to_be_visible()

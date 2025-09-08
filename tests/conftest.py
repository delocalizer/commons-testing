from pathlib import Path
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page, Request
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pytest import Config, TempPathFactory


TIER1 = "tier1"  # anonymous
TIER2 = "tier2"  # registered
TIER3 = "tier3"  # controlled

# Map roles to env var names (username/password)
ROLE_ENV = {
    TIER2: ("USER_TIER2_USERNAME", "USER_TIER2_PASSWORD"),
    TIER3: ("USER_TIER3_USERNAME", "USER_TIER3_PASSWORD"),
}


# Load local env file for developer convenience; CI should rely on real env vars.
load_dotenv(Path(os.getenv("ENV_FILE", ".env")), override=True)


class Settings(BaseSettings):

    # Non-secret
    BASE_URL: str

    # Secret
    USER_TIER2_USERNAME: SecretStr | None
    USER_TIER2_PASSWORD: SecretStr | None
    USER_TIER3_USERNAME: SecretStr | None = None  # not yet configured
    USER_TIER3_PASSWORD: SecretStr | None = None  # not yet configured

    model_config = SettingsConfigDict(
        env_prefix="", case_sensitive=True, extra="ignore"
    )


def perform_login(
    page: Page, settings: Settings, username: SecretStr, password: SecretStr
) -> None:
    """
    Log in with credentials.
    """
    # NOTE
    # This is for the Auth0 Lock flow as currently configured for Gen3.
    # Details will differ for other configurations and other IdPs .
    page.goto(settings.BASE_URL)
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="LOGIN", exact=True).click()
    page.get_by_role("textbox", name="Email address").fill(username.get_secret_value())
    page.get_by_role("textbox", name="Password").fill(password.get_secret_value())
    page.get_by_role("button", name="Continue", exact=True).click()
    page.wait_for_url(f"{settings.BASE_URL}**")


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    s = Settings()
    return s


@pytest.fixture(scope="session")
def auth_storage_states(
    settings: Settings, tmp_path_factory: TempPathFactory, browser: Browser
) -> dict[str, Path | None]:
    """
    Returns {role: storage_state_path or None}. For tier1 (anonymous) the value is None.
    For tier2/tier3: logs in once per session (if creds exist) and saves storage state.
    """
    states: dict[str, Path | None] = {TIER1: None}

    for role, (u_key, p_key) in ROLE_ENV.items():
        username = getattr(settings, u_key, None)
        password = getattr(settings, p_key, None)
        if not (username and password):
            # no creds: skip tests that request this role
            continue
        state_dir = tmp_path_factory.mktemp(f"state_{role}")
        state_file = state_dir / "auth.json"
        ctx = browser.new_context()
        page = ctx.new_page()
        perform_login(page, settings, username, password)
        ctx.storage_state(path=str(state_file))
        ctx.close()
        states[role] = state_file

    return states


@pytest.fixture
def page_as_role(
    request: Request, browser: Browser, auth_storage_states: dict[str, Path | None]
) -> Page:
    """
    A page as seen by a user with the marked role.
    """
    role = getattr(request, "param", TIER1).lower()
    if role not in (TIER1, TIER2, TIER3):
        pytest.fail(f"Unknown role: {role!r}")

    state_path = auth_storage_states.get(role)  # None for tier1 or missing creds
    if role in (TIER2, TIER3) and state_path is None:
        pytest.skip(
            f"Missing credentials for {role}; set {ROLE_ENV[role][0]} and {ROLE_ENV[role][1]}."
        )

    ctx = (
        browser.new_context()
        if state_path is None
        else browser.new_context(storage_state=str(state_path))
    )
    p = ctx.new_page()
    try:
        yield p
    finally:
        p.close()
        ctx.close()


def pytest_configure(config: Config) -> None:
    """
    Show custom markers
    """
    config.addinivalue_line(
        "markers", "auth0: depends on details of Auth0 configuration"
    )
    config.addinivalue_line("markers", "datamodel: depends on details of data model")
    config.addinivalue_line(
        "markers", "role(name): run test as one of: tier1, tier2, tier3"
    )
    config.addinivalue_line("markers", "smoke: is the data commons live")

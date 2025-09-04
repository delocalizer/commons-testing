from pathlib import Path
import os
import pytest
from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load local env file for developer convenience; CI should rely on real env vars.
load_dotenv(Path(os.getenv("ENV_FILE", ".env")), override=True)

class Settings(BaseSettings):

    # Non-secret
    BASE_URL: str

    # Secret
    USER_TIER2_USERNAME: SecretStr | None
    USER_TIER2_PASSWORD: SecretStr | None

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=True,
        extra="ignore"
    )


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    s = Settings()
    return s

Standalone Playwright + pytest E2E tests for a deployed data commons.

Test status for the GitHub actions workflow:

[![e2e](https://github.com/delocalizer/gen3-testing/actions/workflows/e2e.yml/badge.svg)](https://github.com/delocalizer/gen3-testing/actions/workflows/e2e.yml)

You can also run these tests in a local environment:

## Setup

```
# (clone this repo and cd into it)
poetry install --only test
poetry run python -m playwright install   # first time only
```

Settings are taken from environment variables. When run locally (*i.e.* not in
a CI environment) it is often convenient to provide these via `dotenv`:
```
cp .env.example .env
```
and update with your values.

## Run

```
poetry run pytest [--headed]
```

To run all tests conditional on smoke test passing:
```
poetry run pytest -m smoke && poetry run pytest -m "not smoke"
```

----
Reports are written to `playwright-report/`.

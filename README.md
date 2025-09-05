Standalone Playwright + pytest E2E tests for a deployed data commons.

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

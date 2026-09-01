# noted;

Noted is an early Flask e-commerce learning project for a fictional digital-stationery shop. It is being rehabilitated as a safe, reproducible CV demonstration—not as a production store.

The inspected source includes catalogue browsing, accounts, a database-backed cart, discounts, a simulated checkout, order history, admin catalogue/order/stock tools, email templates, invoice services, and notebook-based analytics experiments. See [Project status](docs/PROJECT_STATUS.md) for the evidence boundary and known limitations.

> Safety: the card option is a simulation. The application does not request or process card numbers, expiry dates, or security codes. Do not use real personal or payment data.

## Current state

The publication history was rewritten and independently verified before the repository was made public on 2026-09-01. The current tree has tests, CI, a containerized local demo, documented asset provenance, and explicit deployment boundaries. Hosting is intentionally deferred until the owner operates a personal VPS.

## Stack

- Python and Flask with Jinja templates
- Flask-SQLAlchemy / SQLAlchemy
- MySQL and PyMySQL
- HTML, CSS, and browser JavaScript
- Flask-Mail
- ReportLab for simple demo invoices
- Optional Jupyter, nbconvert, and pandas for offline analytics experiments
- Pytest, Ruff, pip-audit, GitHub Actions, Docker, and Gunicorn

## Reproducible demo

Requirements: Docker with Compose and a modern browser.

```bash
docker compose up --build
```

Open http://localhost:8080. Mailpit is available at http://localhost:8025. The health probe is http://localhost:8080/health. Set `NOTED_PORT` before starting Compose to choose another host port.

Synthetic demo credentials:

- admin: `admin@example.com` / `DemoOnly!2026`
- customer: `demo01@example.com` / `DemoOnly!2026`

See [Demo and deployment](docs/DEPLOYMENT.md) for reset commands, local Python checks, hosted configuration, and limitations. The Flask development server is not a supported public deployment path.

## Repository structure

```text
noted/          Flask application package
database/       MySQL schema and synthetic demo fixtures
docs/           Architecture, decisions, and status notes
notebooks/      Experimental analytics notebooks
scripts/        Legacy Windows development helpers
requirements.txt
```

## Configuration

Configuration comes from environment variables; see `.env.example`. `.env` files, local databases, caches, generated invoices, and virtual environments are ignored by Git.

## Ownership and assistance

André Escarigo is the sole human author. AI tools assisted with implementation, review, documentation, and repository maintenance.

## Licence status

Code and repository-authored visual assets are available under the MIT License. Documentation is CC BY 4.0. Dependencies retain their own licences; see `THIRD_PARTY_NOTICES.md` and `docs/ASSET_PROVENANCE.md`.

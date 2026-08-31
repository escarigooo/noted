# noted;

Noted is an early Flask e-commerce learning project for a fictional digital-stationery shop. It is being rehabilitated as a safe, reproducible CV demonstration—not as a production store.

The inspected source includes catalogue browsing, accounts, a database-backed cart, discounts, a simulated checkout, order history, admin catalogue/order/stock tools, email templates, invoice services, and notebook-based analytics experiments. See [Project status](docs/PROJECT_STATUS.md) for the evidence boundary and known limitations.

> Safety: the card option is a simulation. The application does not request or process card numbers, expiry dates, or security codes. Do not use real personal or payment data.

## Current state

The repository is temporarily private while historical personal/generated files and visual assets of unknown provenance are removed. It is not yet publication-ready or deployed. Automated tests, CI, containers, and deployment instructions will be added during the current cleanup.

## Stack

- Python and Flask with Jinja templates
- Flask-SQLAlchemy / SQLAlchemy
- MySQL and MySQL Connector/Python
- HTML, CSS, and browser JavaScript
- Flask-Mail
- PDF generation libraries
- Jupyter, Papermill, and pandas for experimental admin analytics

## Local setup (current development workflow)

Requirements: Python 3, MySQL, and a modern browser. The Windows batch scripts are retained temporarily for the original local workflow; a cross-platform container workflow is planned.

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`, replace `SECRET_KEY`, and set `DATABASE_URI` for your MySQL instance.
4. Import `database/db_noted.sql`, then optionally `database/test-content.sql` for synthetic demo data.
5. Start the development server:

   ```bash
   python3 -m noted.app
   ```

The default local URL is `http://127.0.0.1:5000`. Do not use the Flask development server for a public deployment.

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

No redistribution licence is granted yet. A code licence and separate third-party/asset notices will be added only after the provenance audit and asset replacement are complete.

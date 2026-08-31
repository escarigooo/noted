# Project status

Last reviewed: 2026-08-31

## Purpose and ownership

Noted is an early, non-production e-commerce learning project prepared as a portfolio demonstration. André Escarigo is the sole human author. AI tools assisted with code, review, documentation, and repository maintenance; they are tools, not human co-authors.

## Confirmed functionality

The source currently contains:

- a Flask application factory and feature-based blueprints;
- product catalogue pages with categories, collections, and related products;
- user registration, email verification, login, password reset, and account pages;
- a database-backed cart, discount handling, checkout, order history, and account balance;
- admin pages and authenticated admin APIs for catalogue, users, orders, and stock;
- order email templates and invoice-generation services;
- MySQL schema and synthetic demonstration fixtures;
- notebook-driven admin analytics experiments.

These statements describe inspected source code. End-to-end behaviour still needs automated and manual verification against a clean database.

## Known limitations and incomplete work

- This is not a real shop and must not be used for real purchases.
- Card payment is deliberately simulated. No card details are requested, processed, or sent to a payment provider.
- There is no production payment integration.
- CSRF protection is not yet wired into the forms or JSON requests.
- Analytics executes Jupyter notebooks during HTTP requests and needs redesign before production use.
- Invoice generation depends on host tools and writes generated files locally.
- Email delivery needs an external SMTP service; local development can use Mailpit or a similar mail catcher.
- Some admin/email preview routes overlap and need consolidation.
- Automated tests, CI, containers, and a supported deployment configuration are being added separately.
- The current visual assets have documented provenance. The repository remains private until the historical unknown assets are removed by the planned Git history rewrite.

## Technology actually present

Python, Flask, Flask-SQLAlchemy, SQLAlchemy, PyMySQL, Flask-Mail, Werkzeug, Jinja, HTML, CSS, browser JavaScript, PDF-generation libraries, Jupyter/nbconvert, pandas, and MySQL.

## Publication gate

Do not make the repository public or advertise a live demo until all of these are complete:

1. asset provenance and licence records pass final review;
2. Git history is rewritten to remove historical personal PDFs and large unredistributable archives;
3. tests, CI, build, and secret scans pass;
4. a clean demo starts from documented commands with synthetic data only;
5. README, screenshots, links, licence notices, and portfolio claims receive a final factual review.

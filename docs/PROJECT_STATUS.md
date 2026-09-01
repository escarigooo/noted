# Project status

Last reviewed: 2026-09-01

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
- Analytics is calculated from the database; notebooks are isolated offline experiments.
- Invoice generation writes simple ReportLab PDFs to configurable runtime storage.
- Email delivery needs an external SMTP service; local development can use Mailpit or a similar mail catcher.
- Some admin/email preview routes overlap and need consolidation.
- The current smoke/critical-flow suite establishes a 25% coverage floor; broader route and failure-path coverage is still needed.
- The current visual assets have documented provenance, including the original Noted identity designed by André Escarigo. Historical third-party assets without confirmed redistribution rights were removed from reachable branch history.
- Legacy pull requests #1, #8, #9, and #10 reference the old history. The removed identities and orders were fictional school-project fixtures, so no GitHub Support sensitive-data purge is required.

## Technology actually present

Python, Flask, Flask-SQLAlchemy, SQLAlchemy, PyMySQL, Flask-Mail, Werkzeug, Jinja, HTML, CSS, browser JavaScript, ReportLab, optional Jupyter/nbconvert/pandas, Gunicorn, Docker, Pytest, Ruff, and MySQL.

## Publication status

The repository was made public on 2026-09-01 after the owner approved the final cross-review.

Completed publication gates:

- asset provenance and licence records were reviewed;
- reachable Git history was rewritten and independently cloned for verification;
- tests, CI, dependency audit, container build, and complete-history secret scans pass;
- the documented Compose demo starts from deterministic synthetic data.
- README, screenshots, public links, licence notices, and portfolio claims receive one final cross-review.
- the owner explicitly approved public repository visibility.

The source repository may now be linked publicly. Hosted deployment is not a publication requirement: the verified local Compose demo remains the supported demonstration until the owner has a personal VPS. Do not advertise a live-demo URL until that deployment exists and has been verified.

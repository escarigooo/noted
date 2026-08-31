# Third-party notices

The project does not vendor these Python packages. Installing `requirements.txt` downloads them from PyPI, and each remains governed by its own licence. This inventory records direct dependencies audited against official PyPI metadata on 2026-08-31; transitive packages must also be reviewed from the final lock/installation report before a release.

| Dependency | Version | Declared licence | Official metadata |
|---|---:|---|---|
| Flask | 3.1.3 | BSD-3-Clause | https://pypi.org/project/Flask/3.1.3/ |
| Flask-SQLAlchemy | 3.1.1 | BSD-3-Clause | https://pypi.org/project/Flask-SQLAlchemy/3.1.1/ |
| SQLAlchemy | 2.0.52 | MIT | https://pypi.org/project/SQLAlchemy/2.0.52/ |
| Jinja2 | 3.1.6 | BSD-3-Clause | https://pypi.org/project/Jinja2/3.1.6/ |
| Flask-Mail | 0.10.0 | BSD | https://pypi.org/project/Flask-Mail/0.10.0/ |
| PyMySQL | 1.2.0 | MIT | https://pypi.org/project/PyMySQL/1.2.0/ |
| reportlab | 5.0.1 | BSD | https://pypi.org/project/reportlab/5.0.1/ |
| itsdangerous | 2.2.0 | BSD-3-Clause | https://pypi.org/project/itsdangerous/2.2.0/ |
| Werkzeug | 3.1.8 | BSD-3-Clause | https://pypi.org/project/Werkzeug/3.1.8/ |
| python-dotenv | 1.2.3 | BSD-3-Clause | https://pypi.org/project/python-dotenv/1.2.3/ |
| gunicorn | 26.2.0 | MIT | https://pypi.org/project/gunicorn/26.2.0/ |

Optional notebook and development dependencies are pinned separately in `requirements-analytics.txt` and `requirements-dev.txt`; they are not installed in the runtime image. Their licences must remain part of development-environment/SBOM review.


## Browser dependency

| Dependency | Version | Declared licence | Official metadata |
|---|---:|---|---|
| Chart.js | 4.5.1 | MIT | https://www.npmjs.com/package/chart.js/v/4.5.1 |

Chart.js is loaded at runtime from jsDelivr and is not vendored in this repository. A production build should vendor or integrity-pin browser dependencies and retain their licence notices.

System tools such as MySQL, wkhtmltopdf, and native libraries used by WeasyPrint are not included in this table. Their licences and deployed versions must be captured by the container/software-bill-of-materials step.

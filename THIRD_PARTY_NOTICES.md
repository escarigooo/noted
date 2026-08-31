# Third-party notices

The project does not vendor these Python packages. Installing `requirements.txt` downloads them from PyPI, and each remains governed by its own licence. This inventory records direct dependencies audited against official PyPI metadata on 2026-08-31; transitive packages must also be reviewed from the final lock/installation report before a release.

| Dependency | Version | Declared licence | Official metadata |
|---|---:|---|---|
| Flask | 2.2.5 | BSD-3-Clause | https://pypi.org/project/Flask/2.2.5/ |
| Flask-SQLAlchemy | 2.5.1 | BSD-3-Clause | https://pypi.org/project/Flask-SQLAlchemy/2.5.1/ |
| SQLAlchemy | 1.4.46 | MIT | https://pypi.org/project/SQLAlchemy/1.4.46/ |
| Jinja2 | 3.1.6 | BSD-3-Clause | https://pypi.org/project/Jinja2/3.1.6/ |
| Flask-Mail | 0.9.1 | BSD | https://pypi.org/project/Flask-Mail/0.9.1/ |
| PyMySQL | 1.1.2 | MIT | https://pypi.org/project/PyMySQL/1.1.2/ |
| pdfkit | 1.0.0 | MIT | https://pypi.org/project/pdfkit/1.0.0/ |
| WeasyPrint | 59.0 | BSD | https://pypi.org/project/WeasyPrint/59.0/ |
| reportlab | 3.6.13 | BSD | https://pypi.org/project/reportlab/3.6.13/ |
| itsdangerous | 2.1.2 | BSD-3-Clause | https://pypi.org/project/itsdangerous/2.1.2/ |
| Werkzeug | 2.2.3 | BSD-3-Clause | https://pypi.org/project/Werkzeug/2.2.3/ |
| python-dotenv | 1.2.3 | BSD-3-Clause | https://pypi.org/project/python-dotenv/1.2.3/ |
| jupyter | 1.1.1 | BSD | https://pypi.org/project/jupyter/1.1.1/ |
| nbconvert | 7.17.1 | BSD-3-Clause | https://pypi.org/project/nbconvert/7.17.1/ |
| pandas | 3.0.5 | BSD-3-Clause (with bundled-component notices) | https://pypi.org/project/pandas/3.0.5/ |


## Browser dependency

| Dependency | Version | Declared licence | Official metadata |
|---|---:|---|---|
| Chart.js | 4.5.1 | MIT | https://www.npmjs.com/package/chart.js/v/4.5.1 |

Chart.js is loaded at runtime from jsDelivr and is not vendored in this repository. A production build should vendor or integrity-pin browser dependencies and retain their licence notices.

System tools such as MySQL, wkhtmltopdf, and native libraries used by WeasyPrint are not included in this table. Their licences and deployed versions must be captured by the container/software-bill-of-materials step.

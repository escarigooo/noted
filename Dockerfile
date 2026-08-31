FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN addgroup --system noted && adduser --system --ingroup noted noted

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=noted:noted . .
RUN mkdir -p /tmp/noted/invoices && chown -R noted:noted /tmp/noted

USER noted
EXPOSE 8000

CMD ["sh", "-c", "exec gunicorn --no-control-socket --bind 0.0.0.0:${PORT} --workers 2 --threads 2 --timeout 60 wsgi:app"]

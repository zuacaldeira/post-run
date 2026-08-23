# stdlib only -- no pip install, nothing to pin, nothing to audit
FROM python:3.12-alpine
COPY sync.py /app/sync.py
USER nobody
ENTRYPOINT ["python3", "-u", "/app/sync.py"]

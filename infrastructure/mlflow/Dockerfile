FROM python:3.10-slim

ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --retries 10 mlflow psycopg2-binary boto3

EXPOSE 5000

CMD ["mlflow", "server", "--backend-store-uri", "postgresql://microlern:microlern123@postgres:5432/microlern_db","--default-artifact-root", "s3://models","--host", "0.0.0.0"]

FROM python:3.10

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --retries 10 --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5003
CMD ["python", "app.py"]

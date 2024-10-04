FROM python:3.11-slim

RUN python3.11 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /tmp/requirements.txt

RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt
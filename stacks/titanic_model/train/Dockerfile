FROM python:3.11-slim

WORKDIR /root

RUN python3.11 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /tmp/requirements.txt
COPY train.py /root/train.py

RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

ENTRYPOINT ["python3.11", "train.py"]

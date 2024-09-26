FROM python:3.11-slim

COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN python3.12 -m pip install --upgrade pip setuptools wheel
RUN python3.12 -m pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* && rm -fr /root/.cache


ENV PYTHONBUFFERED=TRUE

EXPOSE 8080

CMD ["jupyter", "notebook", "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8080", "--NotebookApp.token=''"]
FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip install --upgrade pip && \
    pip install google-cloud-biqquery pandas jupyter



ENV PYTHONBUFFERED=TRUE

EXPOSE 8080

CMD ["jupyter", "notebook", "--allow-root", "--no-browser", "--ip=0.0.0.0", "--port=8080", "--NotebookApp.token=''"]
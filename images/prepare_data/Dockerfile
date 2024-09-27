FROM python:3.11-slim



RUN python3.11 -m pip install --upgrade pip setuptools wheel

# Gcloud recomends to install de dependencies in the same image layer
RUN python3.11 -m pip install --no-cache-dir \
        google-cloud-bigquery==3.26.0 \
        google-cloud-storage==2.18.2 \
        pandas==2.2.3 \
        scikit-learn==1.5.2

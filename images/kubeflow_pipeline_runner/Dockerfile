FROM kubeflownotebookswg/base

RUN python3.11 -m pip install --upgrade pip setuptools wheel

# Gcloud recomends to install de dependencies in the same image layer
RUN python3.11 -m pip install --no-cache-dir \
        PyYAML==6.0.2 \
        python-box==6.0.2 \
        types-PyYAML==6.0.12.12 \
        google-cloud-aiplatform==1.69.0
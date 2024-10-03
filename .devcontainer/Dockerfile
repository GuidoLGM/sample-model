FROM python:3.11-slim

RUN python3.11 -m pip install --upgrade pip setuptools wheel

# kube flow pipeline run dependencies
COPY /images/kubeflow_pipline/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt


# preprocess data dependencies
COPY /images/preprocess_image/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt
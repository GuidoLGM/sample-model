FROM python:3.11-bullseye

RUN python3.11 -m pip install --upgrade pip setuptools wheel

# kube flow pipeline run dependencies
COPY /images/kubeflow_pipeline/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt


# preprocess data dependencies
COPY /images/prepare_data/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

# model prediction dependencies
COPY /stacks/deploy_model/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

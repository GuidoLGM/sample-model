FROM python:3.11-bullseye

RUN python3.11 -m pip install --upgrade pip setuptools wheel

# kube flow pipeline run dependencies
COPY /images/kubeflow_pipeline/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt


# preprocess data dependencies
COPY /images/prepare_data/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt

# model train dependencies
COPY /stacks/titanic_model/train/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt


# model prediction dependencies
COPY /stacks/titanic_model/deploy/requirements.txt /tmp/requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r /tmp/requirements.txt


RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-cli -y
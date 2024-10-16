
# setup on google cloud
# repository

name: sample-model
format: docker
region: us-central1

# Bucket

name: sample-model-kubeflow-pipeline
multi-region: us


# Bucket

name: titanic-artifacts
multi-region: us

## prepare data image

name: update-docker-data-prepare-image

region: us-central1

description: updates the docker image for model training data preparation

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: images/prepare_data/** .cloudbuild/deploy-docker-image.yaml

cloud ruild configuration file location: .cloudbuild/deploy-docker-image.yaml

_API_NAME: sample-model
_IMAGE_NAME: prepare_data
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: us-central1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com


## custom training image

name: build-custom-train-image

region: us-central1

description: build image for custom titanic training model

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: stacks/titanic_model/train/** .cloudbuild/deploy-custom-pipeline-step.yaml

cloud ruild configuration file location: .cloudbuild/deploy-custom-pipeline-step.yaml

_API_NAME: sample-model
_IMAGE_NAME: titanic_model/train
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: us-central1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## custom deploy image

name: build-custom-batch-predict-image

region: us-central1

description: build image for custom titanic training model

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: stacks/titanic_model/deploy/** .cloudbuild/deploy-custom-pipeline-step.yaml

cloud ruild configuration file location: .cloudbuild/deploy-custom-pipeline-step.yaml

_API_NAME: sample-model
_IMAGE_NAME: titanic_model/deploy
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: us-central1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## kubeflow pipeline image
name: update-kubeflow-pipeline-image

region: us-central1

description: updates the docker image for running compiling kubeflow pipelines

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: images/kubeflow_pipline/** .cloudbuild/deploy-docker-image.yaml

cloud ruild configuration file location: .cloudbuild/deploy-docker-image.yaml

_API_NAME: sample-model
_IMAGE_NAME: kubeflow_pipeline
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: us-central1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## run titanic pipeline

name: run-titanic-pipeline

region: us-central1

description: Run the titanic data pipeline on vertex ai

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: stacks/titanic_model/pipeline.ipynb stacks/titanic_model/config.yaml .cloudbuild/run-kubeflow-notebook.yaml

cloud ruild configuration file location: .cloudbuild/run-kubeflow-notebook.yaml

_API_NAME: sample-model
_PIPELINE_NAME: titanic_model
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: us-central1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com


## schedule prepare data pipeline

name: run-prepare-data-pipeline

region: us-central1

description: Schedule run pipeline trigger

event: pub/sub message

pub/sub topic: projects/pebolas-sandbox/topics/trigger-titanic-pipeline

source: 2nd gen

repository: GuidoLGM-sample-model

branch: main

cloud ruild configuration file location: .cloudbuild/run-kubeflow-notebook.yaml

_API_NAME: sample-model
_IMAGE_NAME: kubeflow_pipeline
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: us-central1
_PIPELINE_NAME: prepare_data

Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

# pub/sub topic

name: trigger-titanic-pipeline

# cloud schedule

name: run-preprocess-pipeline

region: us-central1

description: schedule prepare data pipeline

frequency: 0 12 * * 1

timezone: Brasilia Standard Time (BRT) (sao paulo)

target type: Pub/Sub

topic: projects/pebolas-sandbox/topics/trigger-titanic-pipeline

mesasge body: Trigging re prepare pipeline


# experiment

name: titanic
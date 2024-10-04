# prepare data

# dataset
dataset name: titanic
type: tabular/regression or classification
region: southamerica-east1
source: select a table or view from bigquery
BigQuery path: pebolas-sandbox.titanic.train_data

# vertex AI  Training

dataset: No managed dataset
custom traing

name: sample-model


# Bucket


name: sample-model-train-stack-files

region: southamerica-east1
Object versioning: on

# Bucket


name: sample-model-kubeflow-pipeline

region: southamerica-east1
Object versioning: on

# setup on google cloud

## prepare data image

name: update-docker-data-prepare-image

region: southamerica-east1

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
_SERVICE_REGION: southamerica-east1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## kubeflow pipeline image
name: update-kubeflow-pipeline-image

region: southamerica-east1

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
_SERVICE_REGION: southamerica-east1

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## run prepare data pipeline

name: run-prepare-data-pipeline

region: southamerica-east1

description: Run the prepare data pipeline on vertex ai

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: stacks/prepare_data/prepare_data.ipynb stacks/prepare_data/config.yaml .cloudbuild/run-kubeflow-notebook.yaml

cloud ruild configuration file location: .cloudbuild/run-kubeflow-notebook.yaml

_API_NAME: sample-model
_IMAGE_NAME: kubeflow_pipeline
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: southamerica-east1
_PIPELINE_NAME: prepare_data

build logs on githbu: true
Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## schedule prepare data pipeline

name: run-prepare-data-pipeline

region: southamerica-east1

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
_SERVICE_REGION: southamerica-east1
_PIPELINE_NAME: prepare_data

Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

# Workflow

workflow name: simple-model-lifecycle

region: southamerica-east1

service account: Guido Owner

call log level: errors only


# workbench

name: prepare-data-pipeline

region: southamerica-east1

zone: southamerica-each1-a

machine type: e2-standard-2

time of inactivity before shutdown: 30

# pub/sub topic

name: trigger-titanic-pipeline

# cloud schedule

name: run-preprocess-pipeline

region: southamerica-east1

description: schedule prepare data pipeline

frequency: 0 12 * * 1

timezone: Brasilia Standard Time (BRT) (sao paulo)

target type: Pub/Sub

topic: projects/pebolas-sandbox/topics/trigger-titanic-pipeline

mesasge body: Trigging re prepare pipeline
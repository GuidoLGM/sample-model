# prepare data

# dataset
dataset name: titanic
type: tabular/regression or classification
region: southamerica-east1
source: select a table or view from bigquery
BigQuery path: pebolas-sandbox.titanic.train_data_prepared

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

incluses files filter: images/preprocess_image/Dockerfile

cloud ruild configuration file location: .cloudbuild/deploy-docker-image.yaml

_API_NAME: sample-model
_IMAGE_NAME: prepare_data
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: southamerica-east1


Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com

## kubeflow pipeline image
name: update-kubeflow-pipeline-image

region: southamerica-east1

description: updates the docker image for running compiling kubeflow pipelines

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: images/kubeflow_pipeline_runner/Dockerfile

cloud ruild configuration file location: .cloudbuild/deploy-docker-image.yaml

_API_NAME: sample-model
_IMAGE_NAME: prepare_data
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: southamerica-east1


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
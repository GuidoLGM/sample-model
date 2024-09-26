# setup on google cloud

name: update--docker-data-prepare-image

region: southamerica-east1

description: updates the docker image for model training data preparation

event: push to a branch

source: 2nd gen

repository: GuidoLGM-sample-model

branch: ^main$

incluses files filter: [images/prepare_data/Dockerfile, images/prepare_data/requirements.txt]


_API_NAME: sample-model
_IMAGE_NAME: prepare_data
_PROJECT_ID: pebolas-sandbox
_SERVICE_REGION: southamerica-east1


Service account: ci-cd-service-account@pebolas-sandbox.iam.gserviceaccount.com
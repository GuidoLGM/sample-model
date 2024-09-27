# prepare data

# vertex AI Workbench

name: prepare-data
region: us-central1
Zone: us-central1-a

Use custom container: true

Docker container image: southamerica-east1-docker.pkg.dev/pebolas-sandbox/sample-model/prepare_data:latest

general purpose: E2

machine type: e2-standard-2

enable idle shutdown: 10 minutos

# Bucket


name: sample-model-train-stack-files

region: southamerica-east1


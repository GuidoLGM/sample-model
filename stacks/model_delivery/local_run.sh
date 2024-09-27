#!/bin/bash

gcloud ai custom-jobs local-run \
  --executor-image-uri=southamerica-east1-docker.pkg.dev/pebolas-sandbox/sample-model/prepare_data:latest \
  --local-package-path=./stacks/model_delivery/ \
  --script=prepare_data.py
# sample-model


# setup local

login to your gcloud account

```bash
$ gcloud auth login
```

click on the link: https://account.google.com/... 

login to your account linked with the project

run local code:
```bash
$ gcloud ai custom-jobs local-run \
    --executor-image-uri=<image_from_GCR> \
    --local-package-path=<path_to_package_files> \
    --script=<run_script> \
    --service-account-key-file=<absolute_path_json_credentials> \

```
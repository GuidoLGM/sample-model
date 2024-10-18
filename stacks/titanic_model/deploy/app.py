from flask import Flask, jsonify, request, Response
import pandas as pd
import argparse
import joblib
import os
from google.cloud import storage

app = Flask(__name__)


def fetch_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_gcs_path",
        help="google cloud storage path to the model",
        type=str,
        default="gs://sample-model-kubeflow-pipeline/titanic-pipeline/staging/aiplatform-custom-training-2024-10-17-20:39:01.630/model/model.joblib",
    )

    parser.add_argument(
        "--scaler_gcs_path",
        help="google cloud storage path to the scaler",
        type=str,
        default="gs://sample-model-kubeflow-pipeline/titanic-pipeline/470842673491/titanic-pipeline-20241017203224/prepare-data_8796285917779197952/dataset_artifact",
    )

    args = parser.parse_args()
    return args.__dict__


def fetch_gcs_file(gcs_path: str, file_name: str):
    storage_client = storage.Client()
    bucket_name = gcs_path.split("/")[2]
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("/".join(gcs_path.split("/")[3:]))
    blob.download_to_filename(file_name)
    return joblib.load(file_name)


args = fetch_arguments()

model = fetch_gcs_file(args["model_gcs_path"], "model.joblib")
scaler = fetch_gcs_file(args["scaler_gcs_path"], "scaler.joblib")


@app.route(os.environ["AIP_HEALTH_ROUTE"], methods=["GET"])
def health_check():
    return {"status": "healthy"}


@app.route(os.environ["AIP_PREDICT_ROUTE"], methods=["POST"])
def predict():
    try:
        request_json = request.json
        request_instances = request_json["instances"]
        batch = pd.DataFrame(request_instances)
        columns_to_scale = ["Age", "Fare"]
        batch[columns_to_scale] = scaler.transform(batch[columns_to_scale])
        prediction = model.predict(batch)
        output = {"predictions": [{"result": prediction.tolist()}]}
    except Exception as e:
        output = {"error": str(e)}
    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["AIP_HTTP_PORT"])

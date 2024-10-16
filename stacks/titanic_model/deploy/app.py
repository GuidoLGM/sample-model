from flask import Flask, jsonify, request, Response
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
        default="",
    )

    args = parser.parse_args()
    return args.__dict__


def fetch_gcs_file(gcs_path: str, file_name: str):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(gcs_path)
    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)
    return joblib.load(file_name)


args = fetch_arguments()

model = fetch_gcs_file(args["model_gcs_path"], "model.joblib")
scaler = fetch_gcs_file(args["model_gcs_path"], "scaler.joblib")


@app.route(os.environ["AIP_HEALTH_ROUTE"], methods=["GET"])
def health_check():
    return {"status": "healthy"}


@app.route(os.environ["AIP_PREDICT_ROUTE"], methods=["POST"])
def predict():
    request_json = request.json
    request_instances = request_json["instances"]
    scale_data = scaler.transform(request_instances)
    prediction = model.predict(scale_data)
    output = {"predictions": [{"result": prediction.tolist()}]}
    return jsonify(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

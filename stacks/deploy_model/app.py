import os
import pandas as pd
import pickle as pkl
from google.cloud import storage
from fastapi import FastAPI, HTTPException, Request


app = FastAPI(title="Titanic Survival Prediction API")
gcs_client = storage.Client()

bucket = gcs_client.get_bucket("sample-model-kubeflow-pipeline")


blob = bucket.blob(
    "titanic-pipeline/470842673491/titanic-pipeline-20241003144804/scale-data_6946246072335335424/scaler_artifact"
)
blob.download_to_filename("scaler.pkl")


blob = bucket.blob(
    "titanic-pipeline/470842673491/titanic-pipeline-20241004183710/train-model_-4230843777868103680/model"
)
blob.download_to_filename("model.pkl")

scaler = pkl.load(open("scaler.pkl", "rb"))
model = pkl.load(open("model.pkl", "rb"))

@app.get("/health", status_code=200)
async def health():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(request: Request):

    body = await request.json()
    content = body["instances"]

    data = pd.DataFrame(content)

    output = {"predictions": [{"result": []}]}

    column_to_scale = ["Age", "Fare"]
    data[column_to_scale] = scaler.fit_transform(data[column_to_scale])

    prediction = model.predict(data)

    output["predictions"][0]["result"] = prediction.tolist()

    return output

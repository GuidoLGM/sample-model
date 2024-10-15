import os
import fsspec
import joblib
import logging
import argparse
import pandas as pd

from google.cloud import storage
from google.cloud import aiplatform
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    accuracy_score,
)


"""
To make hyperparamethers tuning you need to add the "cloudml-hypertune" package to the code and pass this parameters to argparse
https://cloud.google.com/vertex-ai/docs/training/containers-overview
"""


def fetch_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--train_data_gcs",
        help="Train dataset file on google cloud storage",
        type=str,
        default=(
            os.environ["AIP_TRAINING_DATA_URI"]
            if "AIP_TRAINING_DATA_URI" in os.environ
            else ""
        ),
    )

    parser.add_argument(
        "--val_data_gcs",
        help="Validation dataset file on google cloud storage",
        type=str,
        default=(
            os.environ["AIP_VALIDATION_DATA_URI"]
            if "AIP_VALIDATION_DATA_URI" in os.environ
            else ""
        ),
    )

    parser.add_argument(
        "--model_gcs_path",
        help="Model file on google cloud storage",
        type=str,
        default=(
            os.environ["AIP_MODEL_DIR"]
            if "AIP_MODEL_DIR" in os.environ
            else ""
        ),
    )

    parser.add_argument(
        "--max_iter",
        type=int,
        help="Maximum number of iterations",
        default=100,
    )

    args = parser.parse_args()
    return args.__dict__


def fetch_data(train_data_path: str, test_data_path: str) -> pd.DataFrame:

    logging.info(f"Fetching train data from {train_data_path}")
    logging.info(f"Fetching test data from {test_data_path}")

    train = pd.read_csv(train_data_path, index_col=False)
    test = pd.read_csv(test_data_path, index_col=False)

    logging.info(f"Data fetched successfully")

    return (
        train.drop("Survived", axis=1),
        train["Survived"],
        test.drop("Survived", axis=1),
        test["Survived"],
    )


def train_model(X_train, y_train, max_iter: int):

    logging.info(f"Training model with max_iter={max_iter}")

    model = LogisticRegression(max_iter=max_iter)

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):

    logging.info(f"Evaluating model")

    y_hat = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_hat)
    precision = precision_score(y_test, y_hat, average="weighted")
    recall = recall_score(y_test, y_hat, average="weighted")
    f1 = f1_score(y_test, y_hat, average="weighted")
    auc = roc_auc_score(y_test, y_hat)

    # Log metrics using Vertex AI SDK
    aiplatform.log_metrics(
        {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "auc": auc,
        }
    )


def save_model(model, gcs_path: str):

    logging.info(f"Saving model locally")

    local_dir = "model.joblib"

    joblib.dump(model, local_dir)

    logging.info(f"Uploading model to {gcs_path}")

    storage_path = os.path.join(gcs_path, local_dir)
    blob = storage.Blob.from_string(storage_path, client=storage.Client())
    blob.upload_from_filename(local_dir)
    logging.info(f"Model uploaded successfully")


if __name__ == "__main__":

    aiplatform.init(experiment="titanic")
    fsspec.core.DEFAULT_EXPAND = True
    logging.basicConfig(level=logging.INFO)

    arguments = fetch_arguments()

    aiplatform.start_run(run_name="train")

    X_train, y_train, X_test, y_test = fetch_data(
        arguments["train_data_gcs"], arguments["val_data_gcs"]
    )

    model = train_model(X_train, y_train, arguments["max_iter"])

    auc = evaluate_model(model, X_test, y_test)

    if arguments["model_gcs_path"] != "":
        save_model(model, arguments["model_gcs_path"])

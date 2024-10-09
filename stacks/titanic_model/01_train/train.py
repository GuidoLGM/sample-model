import os
import joblib
import logging
import argparse
import pandas as pd

from google.cloud import storage

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def fetch_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_gcs_path",
        help="Dataset file on google cloud storage",
        type=str,
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


def fetch_data(gcs_path: str) -> pd.DataFrame:

    logging.info(f"Fetching data from {gcs_path}")

    return pd.read_csv(gcs_path, index=False)


def train_test_split(df: pd.DataFrame):

    X, y = df.drop("Survived", axis=1), df["Survived"]

    logging.info(f"Splitting data into train and test sets")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train, max_iter: int):

    logging.info(f"Training model with max_iter={max_iter}")

    model = LogisticRegression(max_iter=max_iter)

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):

    logging.info(f"Evaluating model")

    y_hat = model.predict(X_test)

    auc = roc_auc_score(y_test, y_hat)

    logging.info(f"Model AUC: {auc}")

    return auc


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

    logging.basicConfig(level=logging.INFO)

    arguments = fetch_arguments()

    data = fetch_data(arguments["data_gcs_path"])

    X_train, X_test, y_train, y_test = train_test_split(data)

    model = train_model(X_train, y_train, arguments["max_iter"])

    auc = evaluate_model(model, X_test, y_test)

    if arguments["model_gcs_path"] != "":
        save_model(model, arguments["model_gcs_path"])

import pickle as pkl
import pandas as pd
from google.cloud import biquery
from google.cloud import storage
from sklearn.preprocessing import StandardScaler


def load_data_from_biquery(
    project_id: str, dataset_id: str, table_id: str
) -> pd.DataFrame:
    """
    Load dataset from BigQuery
    """

    print("Connecting to BigQuery...")
    client = biquery.Client(project=project_id)
    query = f"""
    SELECT *
    FROM `{project_id}.{dataset_id}.{table_id}`
    """
    print(f"Querying {dataset_id}.{table_id} from BigQuery...")
    return client.query(query).to_dataframe()


def prepare_titanic_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare Titanic dataset for model training
    """

    print("Preparing Titanic dataset...")
    data.Age = data.Age.fillna(data.Age.mean())

    data.Embarked = data.Embarked.fillna(data.Embarked.mode()[0])

    data.drop(columns=["Cabin", "Name", "Ticket"], inplace=True)

    data.Sex = data.Sex.map({"male": 0, "female": 1})

    data = pd.get_dummies(data, columns=["Embarked"], drop_first=True)

    print("Titanic dataset has been prepared")
    return data


def scale_titanic_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Scale Titanic dataset for model training
    """
    print("Scaling Titanic dataset...")
    scaler = StandardScaler()
    column_to_scale = ["Age", "Fare"]
    data[column_to_scale] = scaler.fit_transform(data[column_to_scale])
    print("Titanic dataset has been scaled")

    return data, scaler


def save_scaler_locally(scaler: StandardScaler, file_path: str) -> None:
    """
    Save scaler to local
    """
    print(f"Saving scaler to {file_path}...")

    with open(file_path, "wb") as f:
        pkl.dump(scaler, f)

    print(f"Scaler has been saved to {file_path}")


def save_scaler_to_bucket(
    source_file_name: str, project_id: str, bucket_name: str, destination_blob_name: str
) -> None:
    """
    Save scaler to GCS
    """

    print("Connecting to GCS...")
    storage_client = storage.Client(project=project_id)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print(f"Uploading scaler to {destination_blob_name}...")
    blob.upload_from_filename(source_file_name)
    print(f"Scaler has been uploaded to {destination_blob_name}")


def save_data_to_bigquery(
    data: pd.DataFrame, project_id: str, dataset_id: str, table_id: str
) -> None:
    """
    Save dataset to BigQuery
    """

    client = biquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    job = client.load_table_from_dataframe(data, table_ref)

    job.result()

    print(f"Dataset {dataset_id}.{table_id} has been saved to BigQuery")


def main():

    PROJECT_ID = "pebolas-sandbox"
    DATASET_ID = "titanic"
    TABLE_ID = "train_data"
    BUCKET_NAME = "sample-model-train-stack-files"
    SCALER_FILE_PATH = "scaler.pkl"
    SCALER_GCS_PATH = "preprocessing/scaler.pkl"
    OUTPUT_DATASET_ID = "titanic"
    OUTPUT_TABLE_ID = "train_data_prepared"

    data = load_data_from_biquery(PROJECT_ID, DATASET_ID, TABLE_ID)

    data = prepare_titanic_data(data)

    data, scaler = scale_titanic_data(data)

    save_scaler_locally(scaler, SCALER_FILE_PATH)

    save_scaler_to_bucket(SCALER_FILE_PATH, PROJECT_ID, BUCKET_NAME, SCALER_GCS_PATH)

    save_data_to_bigquery(data, PROJECT_ID, OUTPUT_DATASET_ID, OUTPUT_TABLE_ID)


if __name__ == "__main__":
    main()

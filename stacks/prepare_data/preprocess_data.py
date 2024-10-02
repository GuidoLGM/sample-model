import pandas as pd
import pickle as pkl
from google.cloud import bigquery
from sklearn.preprocessing import StandardScaler
from kfp.dsl import Input, Output, Artifact, BigQueryTable
from kfp import dsl


class PerprocessData:

    def __init__(
        self,
        project_id: str,
        dataset_id: str,
        table_id: str,
        output_table_id: str,
    ):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.output_table_id = output_table_id

    def connect_to_bigquery(self):
        """
        Connect to BigQuery Client
        """

        print("Connecting to BigQuery...")

        self.client = bigquery.Client(project=self.project_id)

        print("Connected to BigQuery")

    def fetch_data(self):
        """
        Fetch data from BigQuery
        """

        query = f"""
        SELECT *
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
        """

        print(f"Querying {self.dataset_id}.{self.table_id} from BigQuery...")
        self.data = self.client.query(query).result().to_dataframe()

        print("Data fetched successfully")

    def preprocess_titanic_data(self):
        """
        Preprocess Titanic data
        """
        print("Preprocessing Titanic data...")

        self.data.Age = self.data.Age.fillna(self.data.Age.mean())

        self.data.Embarked = self.data.Embarked.fillna(
            self.data.Embarked.mode()[0]
        )

        self.data.drop(columns=["Cabin", "Name", "Ticket"], inplace=True)

        self.data.Sex = self.data.Sex.map({"male": 0, "female": 1})

        self.data = pd.get_dummies(
            self.data, columns=["Embarked"], drop_first=True
        )

        print("Titanic data preprocessed successfully")

    def load_scaler(self) -> None:
        """
        Load scaler
        """
        print("Loading scaler...")
        self.scaler = StandardScaler()
        print("Scaler loaded successfully")

    def scale_data(self) -> None:
        """
        Scale data
        """
        print("Scaling data...")
        column_to_scale = ["Age", "Fare"]
        self.data[column_to_scale] = self.scaler.fit_transform(
            self.data[column_to_scale]
        )
        print("Data scaled successfully")

    def upload_data(self):
        """
        Upload data to BigQuery
        """
        print("Saving data to BigQuery...")

        table_ref = self.client.dataset(self.config.dataset_id).table(
            self.config.output_table_id
        )
        job = self.client.load_table_from_dataframe(self.data, table_ref)
        job.result()

        print("Data saved successfully")

    def save_scaler(self):
        """
        Save scaler to Google Cloud Storage
        """
        scaler_artifact = Artifact(uri=dsl.get_uri())
        with open(scaler_artifact.path, "wb") as f:
            pkl.dump(self.scaler, f)

        return scaler_artifact

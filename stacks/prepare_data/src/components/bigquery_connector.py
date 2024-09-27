import pandas as pd
from google.cloud import bigquery

from entity.config_entity import BigQueryConfig


class BigQueryConnector:

    def __init__(self, config: BigQueryConfig):
        self.config = config
        self.client = None

    def connect(self):
        """
        Connect to BigQuery Client
        """

        self.client = bigquery.Client(project=self.config.project_id)
        print("Connected to BigQuery")

    def fetch_data(self):
        """
        Fetch data from BigQuery
        """

        query = f"""
        SELECT *
        FROM `{self.config.project_id}.{self.config.dataset_id}.{self.config.table_id}`
        """
        print(
            f"Querying {self.config.dataset_id}.{self.config.table_id} from BigQuery..."
        )

        self.data = self.client.query(query).result().to_dataframe()

        print("Data fetched successfully")

    def save_data_locally(self) -> None:
        """
        Save data locally
        """
        print("Saving data locally...")
        self.data_file_path = self.config.root_dir / self.config.data_file
        self.data.to_csv(self.data_file_path)

        print("Scaler saved locally successfully")

    def load_postprocessed_data(self) -> None:
        """
        Load postprocessed data
        """
        print("Loading postprocessed data...")
        self.data = pd.read_csv(
            self.config.postprocessed_data_path, index_col=0
        )
        print("Postprocessed data loaded successfully")

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

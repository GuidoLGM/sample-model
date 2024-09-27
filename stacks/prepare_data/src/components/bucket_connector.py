from google.cloud import storage

from entity.config_entity import BucketConfig


class BucketConnector:

    def __init__(self, config: BucketConfig):
        self.config = config

    def save_data_to_bucket(self):
        """
        Save data to Google Cloud Storage
        """

        print("Saving data to Google Cloud Storage...")
        self.client = storage.Client(project=self.config.project_id)

        bucket = self.client.bucket(self.config.bucket_name)
        blob = bucket.blob(self.config.scaler_gcs_path)

        print(f"Saving scaler to {self.config.scaler_gcs_path}")
        blob.upload_from_filename(self.config.scaler_file_path)
        print("Scaler saved successfully")

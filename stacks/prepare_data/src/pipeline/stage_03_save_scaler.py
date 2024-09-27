from config.configuration import ConfigurationMenager
from components.bucket_connector import BucketConnector

STAGE_NAME = "Save Scaler to Bucket"


class BucketConnectorPipeline:

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        config_menager = ConfigurationMenager()
        bucket_config = config_menager.get_bucket_config()

        bucket = BucketConnector(config=bucket_config)
        bucket.save_data_to_bucket()


if __name__ == "__main__":
    print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)

    obj = BucketConnectorPipeline()
    obj.main()

    print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)

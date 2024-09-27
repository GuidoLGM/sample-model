from config.configuration import ConfigurationMenager
from components.bigquery_connector import BigQueryConnector

STAGE_NAME = "Upload data to BigQuery"


class SaveBigQueryConnectorPipeline:

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        config_menager = ConfigurationMenager()
        bigquery_config = config_menager.get_bigquery_config()

        bigquery_connector = BigQueryConnector(config=bigquery_config)
        bigquery_connector.connect()
        bigquery_connector.load_postprocessed_data()
        bigquery_connector.upload_data()


if __name__ == "__main__":
    print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)

    obj = SaveBigQueryConnectorPipeline()
    obj.main()

    print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)

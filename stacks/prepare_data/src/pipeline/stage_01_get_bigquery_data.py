from config.configuration import ConfigurationMenager
from components.bigquery_connector import BigQueryConnector

STAGE_NAME = "Get BigQuery Data"


class BigQueryConnectorPipeline:

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        config_menager = ConfigurationMenager()
        bigquery_config = config_menager.get_bigquery_config()

        bigquery_connector = BigQueryConnector(config=bigquery_config)
        bigquery_connector.connect()
        bigquery_connector.fetch_data()
        bigquery_connector.save_data_locally()


if __name__ == "__main__":
    print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)

    obj = BigQueryConnectorPipeline()
    obj.main()

    print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)

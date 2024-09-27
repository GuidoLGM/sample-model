from pathlib import Path

from constants import CONFIG_FILE_PATH
from utils.common import read_yaml, create_directories

from entity.config_entity import BigQueryConfig
from entity.config_entity import DataPreprocessorConfig
from entity.config_entity import BucketConfig


class ConfigurationMenager:

    def __init__(self, config_filepath=CONFIG_FILE_PATH) -> None:

        self.config = read_yaml(config_filepath)

        create_directories([self.config.artifacts_root])

    def get_bigquery_config(self) -> BigQueryConfig:

        config = self.config.bigquery_connector
        preprocess_config = self.config.data_preprocessor
        gcp_config = self.config.gcp_config

        create_directories([config.root_dir])

        bigquery_connector_config = BigQueryConfig(
            root_dir=Path(config.root_dir),
            data_file=config.data_file,
            project_id=gcp_config.project_id,
            dataset_id=config.dataset_id,
            table_id=config.table_id,
            output_table_id=config.output_table_id,
            postprocessed_data_path=Path(preprocess_config.root_dir)
            / preprocess_config.postprocessed_data_file,
        )

        return bigquery_connector_config

    def get_data_preprocessor_config(self) -> DataPreprocessorConfig:

        config = self.config.data_preprocessor
        bigquery_config = self.config.bigquery_connector

        create_directories([config.root_dir])

        data_preprocessor_config = DataPreprocessorConfig(
            root_dir=Path(config.root_dir),
            scaler_file=config.scaler_file,
            data_dir=Path(bigquery_config.root_dir)
            / bigquery_config.data_file,
            postprocessed_data_file=config.postprocessed_data_file,
        )

        return data_preprocessor_config

    def get_bucket_config(self) -> BucketConfig:

        config = self.config.bucket_connector
        gcp_config = self.config.gcp_config

        data_preprocessor_config = self.config.data_preprocessor

        bucket_config = BucketConfig(
            project_id=gcp_config.project_id,
            scaler_file_path=Path(data_preprocessor_config.root_dir)
            / data_preprocessor_config.scaler_file,
            bucket_name=config.bucket_name,
            scaler_gcs_path=config.scaler_gcs_path,
        )

        return bucket_config

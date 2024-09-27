from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class BigQueryConfig:
    root_dir: Path
    data_file: str
    project_id: str
    dataset_id: str
    table_id: str
    output_table_id: str
    postprocessed_data_path: Path


@dataclass(frozen=True)
class DataPreprocessorConfig:
    root_dir: Path
    scaler_file: str
    data_dir: Path
    postprocessed_data_file: str


@dataclass(frozen=True)
class BucketConfig:
    project_id: str
    scaler_file_path: Path
    bucket_name: str
    scaler_gcs_path: str

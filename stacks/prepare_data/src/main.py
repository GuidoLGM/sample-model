from pipeline.stage_01_get_bigquery_data import BigQueryConnectorPipeline
from pipeline.stage_02_preprocess_data import DataPreprocessorPipeline
from pipeline.stage_03_save_scaler import BucketConnectorPipeline
from pipeline.stage_04_save_bigquery_data import SaveBigQueryConnectorPipeline

STAGE_NAME = "Get BigQuery Data"

print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)
bq_pipeline = BigQueryConnectorPipeline()
bq_pipeline.main()
print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)


STAGE_NAME = "Preprocess Data"

print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)
preprocess_pipeline = DataPreprocessorPipeline()
preprocess_pipeline.main()
print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)


STAGE_NAME = "Preprocess Data"

print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)
preprocess_pipeline = BucketConnectorPipeline()
preprocess_pipeline.main()
print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)

STAGE_NAME = "Upload data to BigQuery"

print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)
obj = SaveBigQueryConnectorPipeline()
obj.main()
print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)

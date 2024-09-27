from config.configuration import ConfigurationMenager
from components.data_preprocessor import DataPreprocessor

STAGE_NAME = "Preprocess Data"


class DataPreprocessorPipeline:

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        config_menager = ConfigurationMenager()
        data_preprocessor_config = (
            config_menager.get_data_preprocessor_config()
        )

        data_preprocessor = DataPreprocessor(config=data_preprocessor_config)
        data_preprocessor.load_data()
        data_preprocessor.load_scaler()

        data_preprocessor.preprocess_titanic_data()
        data_preprocessor.scale_data()

        data_preprocessor.save_scaler_locally()
        data_preprocessor.save_postprocessed_data()


if __name__ == "__main__":
    print(">" * 20, f"Starting Pipeline {STAGE_NAME}", "<" * 20)

    obj = DataPreprocessorPipeline()
    obj.main()

    print(">" * 20, f"Finished Pipeline {STAGE_NAME}", "<" * 20)

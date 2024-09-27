import pandas as pd
import pickle as pkl
from sklearn.preprocessing import StandardScaler

from entity.config_entity import DataPreprocessorConfig


class DataPreprocessor:

    def __init__(self, config: DataPreprocessorConfig):
        self.config = config

    def load_data(self) -> None:
        """
        Load data
        """
        print("Loading data...")
        self.data = pd.read_csv(self.config.data_dir, index_col=0)

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

    def save_postprocessed_data(self) -> None:
        """
        Save postprocessed data
        """
        print("Saving postprocessed data...")
        self.postprocessed_data_file_path = (
            self.config.root_dir / self.config.postprocessed_data_file
        )
        self.data.to_csv(self.postprocessed_data_file_path)
        print("postprocessed data saved successfully")

    def save_scaler_locally(self) -> None:
        """
        Save scaler locally
        """
        print("Saving scaler locally...")
        self.scaler_file_path = self.config.root_dir / self.config.scaler_file
        with open(self.scaler_file_path, "wb") as f:
            pkl.dump(self.scaler, f)

        print("Scaler saved locally successfully")

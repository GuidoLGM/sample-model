import joblib
import numpy as np
import pandas as pd
import os
import pickle


from google.cloud.aiplatform.constants import prediction
from google.cloud.aiplatform.utils import prediction_utils
from google.cloud.aiplatform.prediction.predictor import Predictor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


class TitanicPredictor(Predictor):
    """Default Predictor implementation for Titanic model."""

    def __init__(self) -> None:
        return

    def load(self, artifacts_uri: str) -> None:
        """Load the model from the given URI."""

        # prediction_utils.download_model_artifacts(artifacts_uri)

        self.model = joblib.load(os.path.join(artifacts_uri, "model.joblib"))
        self.scaler = pickle.load(os.path.join(artifacts_uri, "scaler.pkl"))

    def preprocess(self, prediction_input: dict) -> pd.DataFrame:
        instances = prediction_input["instances"]

        data = pd.DataFrame(instances)
        column_to_scale = ["Age", "Fare"]
        data[column_to_scale] = self.scaler.trasnform(data[column_to_scale])

        return data

    def predict(self, instances: pd.DataFrame) -> np.ndarray:
        return self.model.predict(instances)

    def postprocess(self, prediction_output: np.ndarray) -> dict:
        return {"predictions": prediction_output.tolist()}

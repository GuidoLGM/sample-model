import os
import yaml
import joblib
import logging
import argparse
import pandas as pd
from box import ConfigBox

from google.cloud import storage
from google.cloud import aiplatform

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


if __name__ == "__main__":

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    config = ConfigBox(config)

import sys
from pathlib import Path

file = Path(__file__).resolve()
parent , root = file.parent , file.parents[1]
sys.path.append(str(root))

import typing as t
import  joblib
import pandas as pd
from datetime import datetime
from sklearn.pipeline import Pipeline
from time_series_model import __version__  as _version
from time_series_model.config.core import DATASET_DIR , TRAINED_MODEL_DIR , config

print(_version)

# def parse_custom_date(date_str):
#     # Assuming the format is YYYY0MM
#     year = date_str[:4]
#     month = int(date_str[-2:])
#     corrected_date_str = f"{year}{month:02d}"
#     date_obj = datetime.strptime(corrected_date_str, "%Y%m")
#     return date_obj
def parse_custom_date(date_str):
    # Define the expected date format
    expected_format = "%Y-%m"
    # Check if the date_str matches the expected format
    try:
        # Attempt to parse the date_str using the expected format
        date_obj = datetime.strptime(date_str, expected_format)
        return date_obj  # Return the datetime object if successful
    except ValueError:
        # If parsing fails, it means the date_str is not in the expected format
        year = date_str[:4]
        month = int(date_str[-2:])
        corrected_date_str = f"{year}-{month:02d}"
        try:
            date_obj = datetime.strptime(corrected_date_str, expected_format)
            return date_obj  # Return the adjusted datetime object
        except ValueError:
            print(f"Error parsing date: {date_str}. Format is already correct as expected.")
            return date_str


def _load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe

def load_dataset(*,file_name:str)->pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    dataframe['ds'] = dataframe['ds'].astype(str).apply(lambda x:parse_custom_date(x))
    return dataframe

def save_pipeline(*, pipeline_to_persist:Pipeline)->None:
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR/ save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist,save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()

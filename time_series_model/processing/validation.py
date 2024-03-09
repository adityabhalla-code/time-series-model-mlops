import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from time_series_model.config.core import config
# from time_series_model.processing.data_manager import parse_custom_date


def validate_inputs(*,input_df:pd.DataFrame) -> Tuple[pd.DataFrame , Optional[dict]]:
    """Check model inputs for unprocessable values."""
    validated_data = input_df[config.model_config.features].copy()
    validated_data['ds'] = input_df[config.model_config.date_var]
    errors = None
    # expected a list of dictionaries
    records = validated_data.to_dict(orient='records')
    try:
        _ = MultipleDataInputs(inputs=records)
    except ValidationError as error:
        print(f"Errors--{error}")
        errors = error.json()
    return validated_data , errors


class DataInputSchema(BaseModel):
    ds : Optional[str]
    RBOB_Gasoline_t_2: Optional[float]
    US_Corn_t_1: Optional[float]
    US_Cocoa_t_2: Optional[float]
    consumption_t_1: Optional[float]
    Ind_Prod_t_1: Optional[float]
    Unit_labor_t_1: Optional[float]

class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
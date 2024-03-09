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
from time_series_model.processing.data_manager import parse_custom_date


def validate_inputs(*,input_df:pd.DataFrame) -> Tuple[pd.DataFrame , Optional[dict]]:
    """Check model inputs for unprocessable values."""
    input_df['ds'] = input_df['ds'].astype(str).apply(lambda x: parse_custom_date(x))
    validated_data = input_df[config.model_config.features].copy()
    errors = None
    try:
        MultipleDataInputs(validated_data)
    except ValidationError as error:
        print(f"Errors--{error}")
        errors = error.json()
    return validated_data , errors


class DataInputSchema(BaseModel):
    RBOB_Gasoline_t_2: Optional[str]
    US_Corn_t_1: Optional[str]
    US_Cocoa_t_2: Optional[str]
    consumption_t_1: Optional[str]
    Ind_Prod_t_1: Optional[str]
    Unit_labor_t_1: Optional[str]

class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
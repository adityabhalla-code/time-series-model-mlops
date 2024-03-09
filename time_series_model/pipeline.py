import sys
from pathlib import Path


file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline

from time_series_model.config.core import config
from time_series_model.processing.features import ProphetWrapper , DateParserTransformer

timeSeriesPipeline = Pipeline([
    ('date_parser', DateParserTransformer(variable=config.model_config.date_var)),
    ('prophet', ProphetWrapper())
])
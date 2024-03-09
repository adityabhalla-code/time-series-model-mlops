from prophet import Prophet
from sklearn.base import BaseEstimator, RegressorMixin , TransformerMixin
from time_series_model.processing.data_manager import parse_custom_date

class ProphetWrapper(BaseEstimator, RegressorMixin):
    def __init__(self, growth='linear', daily_seasonality=False, seasonality_mode='additive',
                 changepoint_prior_scale=0.1, seasonality_prior_scale=10.0):
        self.growth = growth
        self.daily_seasonality = daily_seasonality
        self.seasonality_mode = seasonality_mode
        self.changepoint_prior_scale = changepoint_prior_scale
        self.seasonality_prior_scale = seasonality_prior_scale
        self.model = None
        self.X = None

    def fit(self, X, y):
        self.X = X.copy()
        self.model = Prophet(
            growth=self.growth,
            daily_seasonality=self.daily_seasonality,
            seasonality_mode=self.seasonality_mode,
            changepoint_prior_scale=self.changepoint_prior_scale,
            seasonality_prior_scale=self.seasonality_prior_scale
        )
        # Custom seasonality and regressors can be added here
        self.model.add_seasonality(name='monthly', period=240, fourier_order=5)
        self.model.add_regressor('RBOB_Gasoline_t_2')
        self.model.add_regressor('US_Corn_t_1')
        self.model.add_regressor('US_Cocoa_t_2')
        # Add more custom seasonality or regressors if needed

        # Fit the model
        self.model.fit(X)
        return self

    def predict(self, X):
        forecast = self.model.predict(X)
        return forecast#['yhat']

    def get_params(self, deep=False):
        return {
            'growth': self.growth,
            'daily_seasonality': self.daily_seasonality,
            'seasonality_mode': self.seasonality_mode,
            'changepoint_prior_scale': self.changepoint_prior_scale,
            'seasonality_prior_scale': self.seasonality_prior_scale
        }

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self

    def make_future_dataframe(self, periods, freq):
        if self.model is None:
            raise ValueError("Model must be fitted before making a future dataframe.")
        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        # include  regressors here in the proper format,
        for column in ['RBOB_Gasoline_t_2', 'US_Corn_t_1', 'US_Cocoa_t_2', 'consumption_t_1', 'Ind_Prod_t_1',
                       'Unit_labor_t_1']:
            if column in self.X.columns:
                last_value = self.X[column].iloc[-1]
                future[column] = last_value
        return future

# Define the custom transformer for date parsing
class DateParserTransformer(BaseEstimator, TransformerMixin):
    def __init__(self,variable:str):
        if not isinstance(variable,str):
            raise ValueError("Variable should be a string")
        self.variable = variable

    def fit(self, X, y=None):
        # Nothing to fit, so just return self
        return self

    def transform(self, X):
        # Apply the date parsing function to the 'ds' column
        X = X.copy()
        X[self.variable] = X[self.variable].astype(str).apply(lambda x: parse_custom_date(x))
        return X
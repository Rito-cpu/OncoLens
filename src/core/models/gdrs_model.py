# Here goes the model for the gdrs
import pandas as pd
from .base_model import BaseModel

class GDRSModel(BaseModel):
    def __init__(
        self
    ):
        super().__init__(
            name="GDRS",
            description="Growth, Death, Resistance and Sensitivity model for tumors."
        )

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.dropna()
        return data
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        pass


"""
USE THIS FOR IMPORTING CLASSES
        import importlib
        import pkgutil
        from models.base_model import BaseModel

        def load_models():
            models = {}
            package = 'models'
            for _, module_name, _ in pkgutil.iter_modules([package]):
                module = importlib.import_module(f"{package}.{module_name}")
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, BaseModel) and cls is not BaseModel:
                        model_instance = cls()
                        models[model_instance.name] = model_instance
            return models
"""
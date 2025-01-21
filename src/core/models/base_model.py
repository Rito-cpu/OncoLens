from abc import ABC, abstractmethod
import pandas as pd

class BaseModel(ABC):
    def __init__(
        self,
        name:str,
        description: str
    ):
        self.name = name
        self.description = description

    @abstractmethod
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        #     preprocess the input data for the model
        pass

    @abstractmethod
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        #     make predictions based on the input data
        pass

import json
import mimetypes
from typing import Any
import numpy as np

from json import JSONEncoder


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

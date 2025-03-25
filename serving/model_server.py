from kfserving import KFModel
import joblib
import numpy as np
import json
from datetime import datetime
import os

class SklearnModel(KFModel):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.model = None

    def load(self):
        self.model = joblib.load("/mnt/models/model.joblib")

    def predict(self, request: dict) -> dict:
        instances = np.array(request["instances"])
        predictions = self.model.predict(instances).tolist()

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": instances.tolist(),
            "prediction": predictions
        }
        os.makedirs("/mnt/logs", exist_ok=True)
        with open("/mnt/logs/predict_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {"predictions": predictions}

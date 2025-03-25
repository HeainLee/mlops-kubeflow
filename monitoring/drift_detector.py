import pandas as pd
import json
from evidently.report import Report
from evidently.metrics import DataDriftPreset
from kfp import Client
from datetime import datetime

def load_current_data():
    with open("logs/predict_log.json") as f:
        logs = [json.loads(line) for line in f]
    df = pd.DataFrame([x["input"] for x in logs])
    return df.tail(100)

def load_reference_data():
    return pd.read_csv("monitoring/reference.csv")

def detect_drift():
    ref = load_reference_data()
    cur = load_current_data()
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref, current_data=cur)
    result = report.as_dict()
    return result['metrics'][0]['result']['dataset_drift']

def trigger_pipeline():
    client = Client(host="http://<kubeflow-host>/pipeline")
    run = client.create_run_from_pipeline_package(
        pipeline_file="output/pipeline.yaml",
        arguments={"model_path": "/model", "threshold": 0.9},
        experiment_name=f"drift-retrain-{datetime.now().isoformat()}"
    )
    print("Pipeline triggered:", run)

if __name__ == "__main__":
    if detect_drift():
        print("[Drift Detected] → Triggering Retraining Pipeline...")
        trigger_pipeline()
    else:
        print("[No Drift] → No Action.")

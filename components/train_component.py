from kfp.components import create_component_from_func

def train_model(model_path: str) -> str:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    import joblib
    import os

    data = load_iris()
    model = RandomForestClassifier()
    model.fit(data.data, data.target)

    os.makedirs(model_path, exist_ok=True)
    model_file = os.path.join(model_path, "model.joblib")
    joblib.dump(model, model_file)
    return model_file

create_component_from_func(
    train_model,
    base_image="python:3.9",
    output_component_file="train_component.yaml"
)

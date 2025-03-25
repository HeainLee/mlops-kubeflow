from kfp.components import create_component_from_func

def evaluate_model(model_path: str, threshold: float = 0.9) -> str:
    import joblib
    from sklearn.datasets import load_iris
    from sklearn.metrics import accuracy_score

    model = joblib.load(model_path)
    data = load_iris()
    preds = model.predict(data.data)
    acc = accuracy_score(data.target, preds)

    print(f"Accuracy: {acc}")
    return "deploy" if acc >= threshold else "skip"

create_component_from_func(
    evaluate_model,
    base_image="python:3.9",
    output_component_file="evaluate_component.yaml"
)

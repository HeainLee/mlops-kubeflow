from kfp.components import create_component_from_func

def deploy_model(decision: str, model_path: str):
    if decision == "deploy":
        import subprocess
        yaml_content = f"""apiVersion: serving.kubeflow.org/v1beta1
kind: InferenceService
metadata:
  name: iris-sklearn
spec:
  predictor:
    containers:
      - name: sklearn-custom
        image: your-registry/sklearn-kserve-logger:latest
        volumeMounts:
          - name: model-volume
            mountPath: /mnt/models
          - name: log-volume
            mountPath: /mnt/logs
    volumes:
      - name: model-volume
        persistentVolumeClaim:
          claimName: model-pvc
      - name: log-volume
        persistentVolumeClaim:
          claimName: log-pvc
"""
        with open("inference_service.yaml", "w") as f:
            f.write(yaml_content)
        subprocess.run(["kubectl", "apply", "-f", "inference_service.yaml"], check=True)
    else:
        print("Model did not meet threshold. Skipping deployment.")

create_component_from_func(
    deploy_model,
    base_image="python:3.9",
    output_component_file="deploy_component.yaml"
)

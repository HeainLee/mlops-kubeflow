from kfp import dsl
from kfp.components import load_component_from_file

train_op = load_component_from_file("../components/train_component.yaml")
eval_op = load_component_from_file("../components/evaluate_component.yaml")
deploy_op = load_component_from_file("../components/deploy_component.yaml")

@dsl.pipeline(
    name="Train-Evaluate-Deploy Pipeline",
    description="A pipeline that trains, evaluates and conditionally deploys a model"
)
def train_eval_deploy_pipeline(model_path: str = "/model", threshold: float = 0.9):
    train_task = train_op(model_path=model_path)
    eval_task = eval_op(model_path=train_task.output, threshold=threshold)
    deploy_op(decision=eval_task.output, model_path=train_task.output)

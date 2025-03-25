from kfp import compiler
from pipeline import train_eval_deploy_pipeline

compiler.Compiler().compile(
    pipeline_func=train_eval_deploy_pipeline,
    package_path="../output/pipeline.yaml"
)

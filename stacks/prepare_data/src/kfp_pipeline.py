import kfp
from kfp import dsl


def prepare_data_op():
    return dsl.ContainerOp(
        name="prepare_data",
        image="southamerica-east1-docker.pkg.dev/pebolas-sandbox/sample-model/prepare_data:",
        command=["python", "main.py"],
        file_outputs={
            "scaler": "/prepare_data/scaler.pkl",
        },
    )

@dsl.pipeline(
    name="Prepare data",
    description="Prepare data for training",
)
def prepare_data_pipeline():
    prepare_data_task = prepare_data_op()

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(prepare_data_pipeline, "prepare_data_pipeline.zip")
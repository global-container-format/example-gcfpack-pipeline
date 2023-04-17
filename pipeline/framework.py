from inspect import signature

class PipelineStageFailedException(RuntimeError):
    pass


FINALIZER_FUNCTIONS = []


def add_finalizer(f):
    FINALIZER_FUNCTIONS.append(f)


def execute_finalizers():
    for f in FINALIZER_FUNCTIONS:
        f()


def _execute_pipeline_stages(pipeline_stages):
    results = {}

    for stage in pipeline_stages:
        stage_name = stage.__name__
        stage_wants_input = bool(signature(stage).parameters)

        print(f"Starting stage {stage_name}...")

        try:
            results[stage_name] = stage(results.copy()) if stage_wants_input else stage()
        except Exception as e:
            raise PipelineStageFailedException(stage_name) from e

    print("Pipeline execution complete.")


def execute_pipeline(pipeline_stages):
    try:
        _execute_pipeline_stages(pipeline_stages)
    finally:
        execute_finalizers()

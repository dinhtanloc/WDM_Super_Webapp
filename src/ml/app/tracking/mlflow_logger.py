import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

def log_metrics(metrics: dict, run_name="rag_run"):
    with mlflow.start_run(run_name=run_name):
        for key, val in metrics.items():
            mlflow.log_metric(key, val)

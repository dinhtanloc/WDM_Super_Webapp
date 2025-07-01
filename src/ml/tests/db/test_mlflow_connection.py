import mlflow
import pytest
from ml.configs.ml_project_configs import settings

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

EXPERIMENT_NAME = "test_experiment_for_unittest"


def test_mlflow_connection():
    """
    Kiểm tra kết nối đến MLflow Tracking Server
    """
    uri = mlflow.get_tracking_uri()
    assert uri.startswith("http"), f"URI không hợp lệ: {uri}"
    print(f"[✔] Connected to MLflow Tracking URI: {uri}")


def test_mlflow_create_experiment():
    """
    Tạo một experiment nếu chưa có
    """
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment is None:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
        assert experiment_id is not None
        print(f"[✔] Experiment '{EXPERIMENT_NAME}' created with ID: {experiment_id}")
    else:
        print(f"[ℹ] Experiment '{EXPERIMENT_NAME}' already exists")


def test_mlflow_log_run():
    """
    Log một run mẫu với metric, param
    """
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    assert experiment is not None, "Experiment chưa được tạo"

    with mlflow.start_run(experiment_id=experiment.experiment_id) as run:
        mlflow.log_param("param1", 5)
        mlflow.log_metric("accuracy", 0.95)

        run_id = run.info.run_id
        assert run_id is not None
        print(f"[✔] Logged run ID: {run_id}")


def test_mlflow_read_run():
    """
    Đọc lại thông tin run vừa log
    """
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    assert experiment is not None

    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    assert not runs.empty, "Không tìm thấy run"

    run = runs.iloc[0]
    acc = float(run["metrics.accuracy"])
    assert acc > 0, "Giá trị accuracy không hợp lệ"
    print(f"[✔] Run ID {run['run_id']} with accuracy={acc}")


def test_mlflow_cleanup():
    """
    (Optional) Xóa experiment nếu cần dọn dẹp
    Ghi chú: MLflow không hỗ trợ xóa hoàn toàn qua API công khai
    """
    print("[ℹ] MLflow không hỗ trợ xoá hoàn toàn experiment qua public API.")

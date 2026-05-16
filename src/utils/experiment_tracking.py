from pathlib import Path
from datetime import datetime
import json

import mlflow


ROOT = Path(__file__).resolve().parents[2]


def setup_mlflow(
    experiment_name: str,
    tracking_uri: str = "file:./mlruns",
) -> None:
    """
    Configure MLflow tracking.
    """

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def log_experiment(
    model_name: str,
    dataset_metadata_path: str | Path,
    metrics: dict,
    params: dict,
    tags: dict | None = None,
    artifacts: list[str] | None = None,
) -> None:
    """
    Log a full experiment to MLflow.
    """

    dataset_metadata_path = Path(dataset_metadata_path)

    with dataset_metadata_path.open("r", encoding="utf-8") as file:
        dataset_metadata = json.load(file)

    with mlflow.start_run(run_name=model_name):

        # =========================================================
        # Dataset metadata
        # =========================================================

        mlflow.log_param(
            "dataset_name",
            dataset_metadata["dataset_name"],
        )

        mlflow.log_param(
            "dataset_version",
            dataset_metadata["logical_version"],
        )

        mlflow.log_param(
            "dataset_hash",
            dataset_metadata["dataset_hash"],
        )

        mlflow.log_param(
            "dataset_rows",
            dataset_metadata["rows"],
        )

        mlflow.log_param(
            "dataset_columns",
            dataset_metadata["columns"],
        )

        # =========================================================
        # Model parameters
        # =========================================================

        mlflow.log_params(params)

        # =========================================================
        # Metrics
        # =========================================================

        mlflow.log_metrics(metrics)

        # =========================================================
        # Tags
        # =========================================================

        if tags:
            mlflow.set_tags(tags)

        # =========================================================
        # Artifacts
        # =========================================================

        mlflow.log_artifact(str(dataset_metadata_path))

        if artifacts:
            for artifact in artifacts:
                artifact_path = Path(artifact)

                if artifact_path.exists():
                    mlflow.log_artifact(str(artifact))

        mlflow.set_tag(
            "logged_at",
            datetime.now().isoformat(timespec="seconds"),
        )

        print("MLflow experiment logged successfully")
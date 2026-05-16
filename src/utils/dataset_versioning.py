from pathlib import Path
from datetime import datetime
import hashlib
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def generate_file_hash(
    file_path: str | Path,
    chunk_size: int = 8192,
) -> str:
    """
    Generate SHA256 hash for a file.
    """

    file_path = Path(file_path)

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def build_dataset_metadata(
    dataset_path: str | Path,
    dataset_name: str,
    logical_version: str,
    pipeline_name: str,
) -> dict:
    """
    Build dataset metadata dictionary.
    """

    dataset_path = Path(dataset_path)

    if not dataset_path.is_absolute():
        dataset_path = ROOT / dataset_path

    df = pd.read_parquet(dataset_path)

    metadata = {
        "dataset_name": dataset_name,
        "logical_version": logical_version,
        "dataset_path": str(dataset_path),
        "dataset_hash": generate_file_hash(dataset_path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "pipeline_name": pipeline_name,
    }

    return metadata


def save_dataset_metadata(
    metadata: dict,
    output_dir: str | Path = "artifacts/metadata",
) -> Path:
    """
    Save dataset metadata JSON.
    """

    output_dir = Path(output_dir)

    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = (
        output_dir
        / f"{metadata['dataset_name']}_{metadata['logical_version']}_metadata.json"
    )

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return output_path


def version_dataset(
    dataset_path: str | Path,
    dataset_name: str,
    logical_version: str,
    pipeline_name: str,
) -> Path:
    """
    Generate and persist dataset metadata.
    """

    metadata = build_dataset_metadata(
        dataset_path=dataset_path,
        dataset_name=dataset_name,
        logical_version=logical_version,
        pipeline_name=pipeline_name,
    )

    metadata_path = save_dataset_metadata(metadata)

    print("Dataset metadata generated")
    print(f"Dataset: {metadata['dataset_name']}")
    print(f"Version: {metadata['logical_version']}")
    print(f"Rows: {metadata['rows']:,}")
    print(f"Columns: {metadata['columns']:,}")
    print(f"Hash: {metadata['dataset_hash'][:12]}...")
    print(f"Metadata saved to: {metadata_path}")

    return metadata_path
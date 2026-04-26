"""Data-loading helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_dataset(dataset_path: str | Path) -> pd.DataFrame:
    """Load the source dataset into a DataFrame."""
    return pd.read_csv(dataset_path)

import os
import requests
import zipfile
import pandas as pd
from pathlib import Path


def create_project_folders():
    folders = [
        "data_raw",
        "data_processed",
        "data_final",
        "models",
        "plots"
    ]

    for folder in folders:
        Path(folder).mkdir(exist_ok=True)

    print("Project folder structure ready.")


def safe_download(url, output_path):
    """
    Download dataset safely with error handling.
    """
    try:
        print(f"Downloading dataset from: {url}")
        r = requests.get(url, stream=True, timeout=60)

        if r.status_code != 200:
            print("Download failed. Status code:", r.status_code)
            return False

        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("Download complete.")
        return True

    except Exception as e:
        print("Download error:", e)
        return False


def unzip_if_needed(zip_path, extract_to):
    """
    Unzip dataset if zip exists.
    """
    zip_path = Path(zip_path)

    if not zip_path.exists():
        print("Zip file not found.")
        return

    Path(extract_to).mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print("Extraction completed.")


def standardize_columns(df):
    """
    Clean and standardize dataset columns.
    """
    df.columns = df.columns.str.lower().str.strip()

    column_map = {
        "voltage_v": "voltage",
        "current_a": "current",
        "temp": "temperature",
        "temp_c": "temperature",
        "soc_%": "soc"
    }

    df = df.rename(columns=column_map)

    return df


def dataset_report(df):
    """
    Print dataset summary.
    """
    print("Dataset shape:", df.shape)
    print("\nColumns:")
    print(df.columns)

    print("\nMissing values:")
    print(df.isnull().sum())
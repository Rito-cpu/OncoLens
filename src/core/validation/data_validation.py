import pandas as pd

from pathlib import Path
from typing import List, Tuple, Dict
from src.core.app_config import EXCEL_EXTENSIONS, CSV_EXTENSIONS
from .data_keywords import EXPECTED_SHEET_NAMES

def load_file(file_path: Path) -> pd.DataFrame:
    """Load CSV file into a dataframe"""

    try:
        if file_path.suffix in CSV_EXTENSIONS:
            return pd.read_csv(file_path)
        elif file_path.suffix in EXCEL_EXTENSIONS:
            return pd.ExcelFile(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    except Exception as err:
        raise ValueError(f"Error while loading file {file_path}: {err}")
    
def validate_sheets(data: pd.ExcelFile) -> bool:
    """validate that the DataFrame contains the required columns"""
    sheet_names = data.sheet_names
    is_subset = set(EXPECTED_SHEET_NAMES).issubset(set(sheet_names))
    if not is_subset:
        raise ValueError(f"Missing the following required sheets: {set(EXPECTED_SHEET_NAMES) - set(sheet_names)}")
    return is_subset

def preprocess_data(file_path: Path, required_columns: List[str]) -> pd.DataFrame:
    """Loads, validates, and preprocesses data from a file."""
    data = load_file(file_path)
    if validate_sheets(data, required_columns):
        return data

def get_file_paths(directory: Path, extensions: List[str]) -> List[Path]:
    """Fetches all file paths in the given directory with the specified extensions."""
    return [file for file in directory.iterdir() if file.suffix in extensions and file.is_file()]

def main(input_directory: Path, output_directory: Path, required_columns: List[str], extensions: List[str] = [".csv", ".xls", ".xlsx"]) -> None:
    """Main workflow to process all files in a directory."""
    input_files = get_file_paths(input_directory, extensions)
    output_directory.mkdir(parents=True, exist_ok=True)

    for file_path in input_files:
        try:
            data = preprocess_data(file_path, required_columns)
            output_file = output_directory / (file_path.stem + ".csv")
            data.to_csv(output_file, index=False)
            print(f"Processed and saved: {output_file}")
        except ValueError as e:
            print(f"Skipping file {file_path} due to error: {e}")

if __name__ == "__main__":
    my_input = input('Enter file path:')

    my_df = load_file(my_input)
    print(my_df)
    validate_sheets(my_df)

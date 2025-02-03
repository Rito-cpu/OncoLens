import pandas as pd

from pathlib import Path
from typing import List, Tuple, Dict
from src.core.app_config import EXCEL_EXTENSIONS, CSV_EXTENSIONS
from .data_keywords import *


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
    
def validate_excel_sheets(data: pd.ExcelFile) -> bool:
    """validate that the DataFrame contains the required columns"""
    sheet_names = data.sheet_names
    is_subset = set(EXPECTED_SHEET_NAMES).issubset(set(sheet_names))
    if not is_subset:
        raise ValueError(f"Missing the following required sheets: {set(EXPECTED_SHEET_NAMES) - set(sheet_names)}")
    return True

def validate_sheet_data(data: pd.ExcelFile) -> bool:
    ########################################
    # * Validate the Non-Critical Sheets * #
    ########################################
    # * Notable Dates Sheet Validation - Non-Critical * #
    notable_dates = data.parse(NOTABLE_DATES_SHEET, header=0)
    # Check if amount of columns match expected headers
    if len(set(notable_dates.columns)) != len(NOTABLE_DATES_HEADERS):
        raise ValueError(f"Notable dates column count does not match expected header count: {NOTABLE_DATES_HEADERS}")
    else:
        # Check if the header names are what we need
        if not NOTABLE_DATES_HEADERS.issubset(set(notable_dates.columns)):
            raise ValueError(f"Notable dates sheet is missing the following headers: {NOTABLE_DATES_HEADERS-set(notable_dates.columns)}")
    
    # * Available Treatments Sheet Validation - Non-Critical * #
    available_treatments = data.parse(AVAILABLE_TX_SHEET, header=0)
    if len(set(available_treatments.columns)) != len(AVAILABLE_TX_HEADERS):
        raise ValueError(f"Available treatment column count does nor match expected header counnt: {AVAILABLE_TX_HEADERS}")
    else:
        if not AVAILABLE_TX_HEADERS.issubset(set(available_treatments.columns)):
            raise ValueError(f"Available treatments sheet is missing the following headers in Available Treatments: {AVAILABLE_TX_HEADERS-set(available_treatments.columns)}")
        if available_treatments.shape[0] > 1:
            column_lengths = [available_treatments[col].notnull().sum() for col in set(available_treatments.columns)]
            if len(set(column_lengths)) > 1:
                raise ValueError(f"Available Treatments columns have unequal row lengths: {column_lengths}")
        
    ####################################
    # * Validate the Critical Sheets * #
    ####################################
    # * Historical Treatment Sheet Validation - Critical Information * #
    historical_treatments = data.parse(HISTORICAL_TX_SHEET, header=0)
    if historical_treatments.empty:
        raise ValueError(f"Historical treatment sheet is empty. Please provide the required headers: {HISTORICAL_TX_HEADERS}")
    elif len(set(historical_treatments.columns)) != len(HISTORICAL_TX_HEADERS):
        raise ValueError(f"Historical treatment column count does not match expected header count: {HISTORICAL_TX_HEADERS}")
    else:
        if not set(historical_treatments.columns).issubset(HISTORICAL_TX_HEADERS):
            raise ValueError(f"Historical treatment sheet is missing the following headers: {HISTORICAL_TX_HEADERS-set(historical_treatments.columns)}")
        if historical_treatments.shape[0] > 1:
            column_lengths = [historical_treatments[col].notnull().sum() for col in historical_treatments.columns]
            if len(set(column_lengths)) > 1:
                raise ValueError(f"Historical Treatments columns have unequal row lengths: {column_lengths}")
        else:
            raise ValueError(f"Historical treatment has no rows of data.")

    # * Clinician Size Data Sheet Validation - Critical Information * #
    scan_data = data.parse(SCAN_DATA_SHEET, header=0)
    if scan_data.empty:
        raise ValueError(f"Scan data sheet is empty. Please provide the required headers: {SCAN_DATA_HEADERS}")
    elif len(scan_data.columns) < 4 :
        raise ValueError(f"Scan data sheet must have at least 4 columns, with the 4th column being scan volumes.")
    else:
        if not set(scan_data.values[0, 0:3]).issubset(SCAN_DATA_HEADERS):
            raise ValueError(f"Scan data sheet is missing the following headers: {SCAN_DATA_HEADERS-set(scan_data.values[0, 0:2])}")
        if scan_data.shape[0] < 1:
            raise ValueError(f"Scan data has no rows of data.")

    return True

def format_data(file_path: Path, data: pd.ExcelFile) -> dict:
    """Formats data into a dictionary."""
    notable_dates = data.parse(NOTABLE_DATES_SHEET, header=0)
    available_treatments = data.parse(AVAILABLE_TX_SHEET, header=0)
    historical_treatments = data.parse(HISTORICAL_TX_SHEET, header=0)
    scan_data = data.parse(SCAN_DATA_SHEET, header=0)
    scan_dates = scan_data.columns.to_list()

    all_data = {
        "data_path": file_path,
        "notable_dates": {
            "headers": notable_dates.columns.to_list(),
            "values": notable_dates.values
        },
        "available_treatments": {
            "headers": available_treatments.columns.to_list(),
            "names": available_treatments.values[:, 0],
            "abbr": available_treatments.values[:, 1]
        },
        "historical_treatments": {
            "headers": historical_treatments.columns.to_list(),
            "names": historical_treatments.values[:, 0],
            "abbr": historical_treatments.values[:, 1],
            "date_on": historical_treatments.values[:, 2],
            "date_off": historical_treatments.values[:, 3],
            "active": historical_treatments.values[:, 4]
        },
        "scan_data": {
            "scan_dates": scan_dates[3:],
            "names": scan_data.values[1:, 0],
            "abbr": scan_data.values[1:, 1],
            "recist": scan_data.values[1:, 2],
            "volumes": scan_data.values[1:, 3:]
        }
    }

    return all_data

def preprocess_data(file_path: Path) -> pd.DataFrame:
    """Loads, validates, and preprocesses data from a file."""
    file_data = load_file(file_path)
    if validate_excel_sheets(file_data) and validate_sheet_data(file_data):
        formatted_data = format_data(file_path, file_data)
        return formatted_data

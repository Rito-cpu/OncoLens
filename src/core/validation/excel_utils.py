import os
import pandas as pd

from src.core.keyword_store import *
from typing import Optional, NamedTuple, Dict


class ExcelCheckResult(NamedTuple):
    """A named tuple to represent the result of Excel file checks."""
    file_warning: bool
    file_warning_message: str
    file_error: bool
    file_error_message: str
    has_data: bool
    data: Dict[str, any]

class ExcelFileError(Exception):
    """Custom exception for Excel file Errors"""

class ExcelFileWarning(Exception):
    """Custom exception for Excel file Warnings"""

class ExcelFileErrorWithWarning(Exception):
    """Custom exception for Excel file with both Errors and Warnings"""

def initiate_excel_check(file_path: str, num_sheets: int=4) -> ExcelCheckResult:
    """
    Initiates the Excel check process.

    Args:
        file_path (str): The path to the Excel file.
        num_sheets (int, optional): The expected number of sheets in the Excel file. Defaults to 4.
        sheet_names (Dict[int, str], optional): Dictionary mapping sheet indices to sheet names.
            Defaults to None.

    Returns:
        ExcelCheckResult: A named tuple representing the result of the Excel file check.
    """

    file_path = os.path.abspath(file_path)

    return valid_file_check(file_path, num_sheets)

def valid_file_check(file_path: str, num_sheets: int) -> dict:
    """Performs a valid file check for an Excel file.

    Args:
        file_path (str): The path to the Excel file.
        num_sheets (int): The expected number of sheets in the Excel file.
        sheet_names (Dict[int, str]): Dictionary mapping sheet indices to sheet names.

    Returns:
        ExcelCheckResult: A named tuple representing the result of the Excel file check.
    """

    if not os.path.exists(file_path):
        raise ExcelFileError('Excel file quick check failed: File does not exist!')

    excel_file = pd.ExcelFile(file_path)
    current_sheet_names = excel_file.sheet_names

    # --- Uneven sheet number ---
    #if len(current_sheet_names) < num_sheets:
    #    raise ExcelFileError('Excel file quick check failed: Length issue!')
    # --- Sheet names are not the same ---
    #elif
    #if not set(SHEET_SET).issubset(set(current_sheet_names)):
    #    raise ExcelFileError('Excel file quick check failed: Sheet name issue!')

    # Correct file passed, proceed with detailed data check
    return file_data_check(file_path, excel_file)

def file_data_check(file_path: str, excel_file) -> ExcelCheckResult:
    if excel_file is None:
        excel_file = pd.ExcelFile(file_path)

    result = ExcelCheckResult(
        file_warning=False,
        file_warning_message="",
        file_error=False,
        file_error_message="",
        has_data=False,
        data={}
    )

    warnings = []
    errors = []

    try:
        # *** Check Unimportant Sheets ***
        # Check for notable dates
        if NOTABLE_DATES_SHEET not in excel_file.sheet_names:
            warnings.append(UNIMPORTANT_SHEET_MISSING_WARNING.format(_sheet_name=NOTABLE_DATES_SHEET))
        else:
            notable_dates_sheet = excel_file.parse(NOTABLE_DATES_SHEET)
            if len(notable_dates_sheet.columns) == 0:
                warnings.append(UNIMPORTANT_ALL_COL_MISSING_WARNING.format(_sheet_name=NOTABLE_DATES_SHEET))
            else:
                # Check if column is included
                for header in NOTABLE_DATES_HEADERS:
                    if header not in notable_dates_sheet.columns:
                        warnings.append(UNIMPORTANT_COL_MISSING_WARNING.format(_sheet_name=NOTABLE_DATES_SHEET, _col_name=header))

        # Check for Available Treatments
        ignore_available_tx = False
        if AVAILABLE_TX_SHEET not in excel_file.sheet_names:
            warnings.append(UNIMPORTANT_SHEET_MISSING_WARNING.format(_sheet_name=AVAILABLE_TX_SHEET))
            ignore_available_tx = True
        else:
            available_treatment_test = excel_file.parse(AVAILABLE_TX_SHEET, header=0)
            if len(available_treatment_test.columns) == 0:
                warnings.append(UNIMPORTANT_ALL_COL_MISSING_WARNING.format(_sheet_name=AVAILABLE_TX_SHEET))
                ignore_available_tx = True
            else:
                # Check if necessary columns are included
                for header in AVAILABLE_TX_HEADERS:
                    if header not in available_treatment_test.columns:
                        warnings.append(UNIMPORTANT_COL_MISSING_WARNING.format(_sheet_name=AVAILABLE_TX_SHEET, _col_name=header))
                # Check if columns are of equal length
                available_tx_col_counts = {}
                for column in available_treatment_test.columns:
                    available_tx_col_counts[column] = len(available_treatment_test.dropna(subset=[column]))

                if len(set(available_tx_col_counts.values())) != 1:
                    ignore_available_tx = True
                    warnings.append(UNIMPORTANT_UNEQUAL_COL_WARNING.format(_sheet_name=AVAILABLE_TX_SHEET))

        # *** Check Critical Sheets ***
        # --- Historical treatment check ---
        if HISTORICAL_TX_SHEET not in excel_file.sheet_names:
            errors.append(CRITICAL_SHEET_MISSING_ERROR.format(_sheet_name=HISTORICAL_TX_SHEET))
        else:
            historical_treatment_test = excel_file.parse(HISTORICAL_TX_SHEET, header=0)
            if len(historical_treatment_test.columns) == 0:
                errors.append(CRITICAL_SHEET_EMPTY_ERROR.format(_sheet_name=HISTORICAL_TX_SHEET))
            else:
                # Check if necessary columns are included
                for header in HISTORICAL_TX_HEADERS:
                    if header not in historical_treatment_test.columns:
                        errors.append(CRITICAL_COL_MISSING_ERROR.format(_sheet_name=HISTORICAL_TX_SHEET, _col_name=header))
                    elif historical_treatment_test[header].isnull().values.any():
                        errors.append(CRITICAL_NULL_COL_ERROR.format(_sheet_name=HISTORICAL_TX_SHEET, _col_name=header))
                # Check if columns from sheet have same length
                historical_tx_col_count = {}
                for column in historical_treatment_test.columns:
                    historical_tx_col_count[column] = len(historical_treatment_test.dropna(subset=[column]))

                if len(set(historical_tx_col_count.values())) != 1:
                    errors.append(CRITICAL_UNEQUAL_COL_ERROR.format(_sheet_name=HISTORICAL_TX_SHEET))

        # --- Clinician data check ---
        if SCAN_DATA_SHEET not in excel_file.sheet_names:
            errors.append(CRITICAL_SHEET_MISSING_ERROR.format(_sheet_name=SCAN_DATA_SHEET))
        else:
            lesion_info_df = pd.read_excel(file_path, sheet_name=SCAN_DATA_SHEET, header=1)
            lesion_data = lesion_info_df.to_numpy()
            print(f'Lesion data:\n{lesion_data}\n\n')

            if lesion_data.shape[0] == 0 or lesion_data.shape[1] <= 3:
                pass
                # sys.exit(f"Clinician data does not meet minimum requirements. Missing values and/or columns.")

            size_data_with_dates = excel_file.parse(SCAN_DATA_SHEET, header=0)
            print(f'Clinician volume data:\n{size_data_with_dates}')
            size_data_with_headers = excel_file.parse(SCAN_DATA_SHEET, header=1, usecols=lambda x: 'Volume' not in x)
            for header in SCAN_DATA_HEADERS:
                if header not in size_data_with_headers.columns:
                    errors.append(CRITICAL_COL_MISSING_ERROR.format(_sheet_name=SCAN_DATA_SHEET, _col_name=header))
                elif size_data_with_headers[header].isnull().values.any():
                    errors.append(f'Column \'{header}\' in sheet \'{SCAN_DATA_SHEET}\' contains an empty value - uneven column size!')

        if errors and not warnings:
            raise ExcelFileError('\n'.join(errors))
        elif not errors and warnings:
            data_dict = {
                'excel_file_path': file_path,
                'lesion_data': {
                    'Name': size_data_with_headers['Name'],
                    'Abbr': size_data_with_headers['Abbr']
                },
                'historical_treatment_data': {
                    'Name': historical_treatment_test['Name'],
                    'Abbr': historical_treatment_test['Abbr'],
                    'On': historical_treatment_test['Date On'],
                    'Off': historical_treatment_test['Date Off']
                },
                'available_treatment_data': {
                    'Name': available_treatment_test['Name'] if not ignore_available_tx else None,
                    'Abbr': available_treatment_test['Abbr'] if not ignore_available_tx else None
                }
            }
            result = result._replace(has_data=True, data=data_dict)
            raise ExcelFileWarning('\n'.join(warnings))
        elif errors and warnings:
            raise ExcelFileErrorWithWarning('\n'.join(errors+warnings))

        # Populate the 'data' dictionary with the required information
        # Create a new instance with updated values
        data_dict = {
            'excel_file_path': file_path,
            'lesion_data': {
                'Name': size_data_with_headers['Name'],
                'Abbr': size_data_with_headers['Abbr']
            },
            'historical_treatment_data': {
                'Name': historical_treatment_test['Name'],
                'Abbr': historical_treatment_test['Abbr'],
                'On': historical_treatment_test['Date On'],
                'Off': historical_treatment_test['Date Off']
            },
            'available_treatment_data': {
                'Name': available_treatment_test['Name'] if not ignore_available_tx else None,
                'Abbr': available_treatment_test['Abbr'] if not ignore_available_tx else None
            }
        }
        result = result._replace(has_data=True, data=data_dict)

    except ExcelFileError as efe:
        result = result._replace(file_error=True, file_error_message=str(efe))
    except ExcelFileWarning as efw:
        result = result._replace(file_warning=True, file_warning_message=str(efw))
    except ExcelFileErrorWithWarning as ef:
        result = result._replace(file_error=True, file_warning=True, file_error_message=str(ef))

    return result

def has_file_error(file_obj: ExcelCheckResult):
    return file_obj.file_error

def has_file_warning(file_obj: ExcelCheckResult):
    return file_obj.file_warning

def has_file_error_and_warning(file_obj: ExcelCheckResult):
    return (file_obj.file_error and file_obj.file_warning)

def get_settings_data(file_obj: ExcelCheckResult):
    return file_obj.data

def get_file_path(file_obj: ExcelCheckResult):
    return file_obj.data["excel_file_path"]

def get_error_message(file_obj: ExcelCheckResult):
    return file_obj.file_error_message
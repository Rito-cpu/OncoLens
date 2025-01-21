# Keyword Storage for Modularity

# **** Excel Keys ****
NOTABLE_DATES_SHEET: str = "notable_dates"
HISTORICAL_TX_SHEET: str = "historical_tx"
AVAILABLE_TX_SHEET: str = "available_tx"
SCAN_DATA_SHEET: str = "scan_data"

NOTABLE_DATES_HEADERS = ['ETBdates', 'NextScans', 'Expired']
HISTORICAL_TX_HEADERS = ['Name', 'Abbr', 'Date On', 'Date Off', 'Active']
AVAILABLE_TX_HEADERS = ['Name', 'Abbr']
SCAN_DATA_HEADERS = ['Name', 'Abbr', 'RECIST']

SHEET_SET: list = [NOTABLE_DATES_SHEET, HISTORICAL_TX_SHEET, AVAILABLE_TX_SHEET, SCAN_DATA_SHEET]

# **** EXCEL WARNINGS ****
UNIMPORTANT_SHEET_MISSING_WARNING = "Warning: The sheet \'{_sheet_name}\' is not present in the excel file provided. Modeling/plotting will continue without the functionality of the missing sheet."
UNIMPORTANT_COL_MISSING_WARNING = "Warning: The sheet \'{_sheet_name}\' does not have the right columns (\'{_col_name}\'). Modeling/plotting will continue as normal without the use of the sheet."
UNIMPORTANT_ALL_COL_MISSING_WARNING = "Warning: The sheet \'{_sheet_name}\' has no columns (empty sheet). Modeling/plotting will continue as normal without the use of the sheet."
UNIMPORTANT_UNEQUAL_COL_WARNING = "Warning: The sheet \'{_sheet_name}\' has unequal columns. Please use an equal amount of data in each column to utilize the sheet. Modeling/plotting will continue as normal without the use of the sheet."

# **** EXCEL ERRORS ****
CRITICAL_SHEET_MISSING_ERROR = "Error: The sheet \'{_sheet_name}\' is not present in the excel file provided! Please create this sheet, since it is necessary in order to continue. If the sheet with the data already exists, make sure the sheet name is set to \'{_sheet_name}\'"
CRITICAL_COL_MISSING_ERROR = "Error: The sheet \'{_sheet_name}\' is missing a critical column: (\'{_col_name}\')!. Please add this column to continue. If column exists, then please rename to \'{_col_name}\'"
CRITICAL_NULL_COL_ERROR = "Error: The sheet \'{_sheet_name}\' has a null value(s) in column (\'{_col_name}\')! Please make sure all data columns have equal length in order to continue."
CRITICAL_MISSING_DATES_ERROR = "Error: The sheet \'{_sheet_name}\' has its dates row empty! Please add dates to this row, according to the sheet format, to continue."
CRITICAL_SHEET_EMPTY_ERROR = "Error: The sheet \'{_sheet_name}\' has no columns (empty sheet). Please poppulate this sheet with appropriate data according to the required excel format."
CRITICAL_UNEQUAL_COL_ERROR = "Error: The sheet \'{_sheet_name}\' has unequal columns. Please make sure an equal amount of data is contained since this sheet is critical to proceed."

# **** Modeling Constants ****
DETECT_SIZE: float = 3e6/1e9
DETECT_LINE: float = 0.003
DEATH_THRESHOLD: float = 1e-11

# **** Cone Modes ****
NO_CONE: str = "No Cone"
COMBINATION_CONE: str = "Combination Cone"
COMPARISON_CONE: str = "Comparison Cone"

# **** SQL Commands ****
SELECT_COMMAND = 'SELECT'
ALL_COMMAND = '*'
FROM_COMMAND = 'FROM'
USE_COMMAND = 'USE'
INSERT_COMMAND = 'INSERT'
INTO_COMMAND = 'INTO'
VALUES_COMMAND = 'VALUES'
UPDATE_COMMAND = 'UPDATE'
SET_COMMAND = 'SET'
WHERE_COMMAND = 'WHERE'
ORDER_BY_COMMAND = 'ORDER BY'
ASC_COMMAND = 'ASC'
DESC_COMMAND = 'DESC'
LIMIT_COMMAND = 'LIMIT'
DELETE_COMMAND = 'DELETE'
DROP_COMMAND = 'DROP'
CREATE_COMMAND = 'CREATE'
DATABASE_COMMAND = 'DATABASE'
TABLE_COMMAND = 'TABLE'
PRIMARY_KEY_COMMAND = 'PRIMARY KEY'
FOREIGN_KEY_COMMAND = 'FOREIGN KEY'
REFERENCES_COMMAND = 'REFERENCES'
NOT_NULL_COMMAND = 'NOT NULL'
UNIQUE_COMMAND = 'UNIQUE'
DEFAULT_COMMAND = 'DEFAULT'
NULL_COMMAND = 'NULL'
AUTO_INCREMENT_COMMAND = 'AUTO_INCREMENT'


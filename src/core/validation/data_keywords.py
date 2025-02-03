# **** Excel Sheets ****
NOTABLE_DATES_SHEET: str = "notable_dates"
HISTORICAL_TX_SHEET: str = "historical_tx"
AVAILABLE_TX_SHEET: str = "available_tx"
SCAN_DATA_SHEET: str = "scan_data"
EXPECTED_SHEET_NAMES: set[str] = {NOTABLE_DATES_SHEET, AVAILABLE_TX_SHEET, HISTORICAL_TX_SHEET, SCAN_DATA_SHEET}

# **** Excel Headers ****
NOTABLE_DATES_HEADERS: set = {'ETBdates', 'NextScans', 'Expired'}
HISTORICAL_TX_HEADERS: set = {'Name', 'Abbr', 'Date On', 'Date Off', 'Active'}
AVAILABLE_TX_HEADERS: set = {'Name', 'Abbr'}
SCAN_DATA_HEADERS: set = {'Name', 'Abbr', 'RECIST'}
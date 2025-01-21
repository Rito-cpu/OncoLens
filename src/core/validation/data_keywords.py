# **** Excel Keys ****
NOTABLE_DATES_SHEET: str = "notable_dates"
HISTORICAL_TX_SHEET: str = "historical_tx"
AVAILABLE_TX_SHEET: str = "available_tx"
SCAN_DATA_SHEET: str = "size_data"
EXPECTED_SHEET_NAMES: list[str] = [NOTABLE_DATES_SHEET, HISTORICAL_TX_SHEET, AVAILABLE_TX_SHEET, SCAN_DATA_SHEET]

NOTABLE_DATES_HEADERS = ['ETBdates', 'NextScans', 'Expired']
HISTORICAL_TX_HEADERS = ['Name', 'Abbr', 'Date On', 'Date Off', 'Active']
AVAILABLE_TX_HEADERS = ['Name', 'Abbr']
SCAN_DATA_HEADERS = ['Name', 'Abbr', 'RECIST']
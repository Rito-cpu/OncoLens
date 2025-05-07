import sys
import pathlib


# --- Directory Settings ---
if getattr(sys, 'frozen', False):
    # If running as pyinstaller packaged app
    APP_ROOT = pathlib.Path(sys._MEIPASS)
else:
    # Project root directory
    APP_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# --- Image resources directory ---
image_dir = "resources/images"
IMG_RSC_PATH = APP_ROOT / image_dir

# --- Excel File Data ---
EXCEL_EXTENSIONS: list[str] = [".xlsx", ".xls"]
CSV_EXTENSIONS: list[str] = [".csv"]
current_excel_path: str = None

# --- Home Directory Instance ---
working_directory = None

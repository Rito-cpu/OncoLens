import os
import pathlib


# --- Directory Settings ---
APP_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

resources_dir = "resources"
images_dir = "images"
IMG_RSC_PATH = APP_ROOT / resources_dir / images_dir

# --- Excel File Data ---
EXCEL_EXTENSIONS: list[str] = [".xlsx", ".xls"]
CSV_EXTENSIONS: list[str] = [".csv"]
current_excel_path: str = None

# --- Home Directory Instance ---
working_directory = None
